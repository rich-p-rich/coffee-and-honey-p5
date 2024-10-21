from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse
)
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order, OrderLineItem

from products.models import Product
from profiles.models import RecipientAddresses
from profiles.forms import UserProfileForm
from profiles.models import UserProfile
from bag.contexts import bag_contents

import stripe
import json


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, ('Sorry, your payment cannot be '
                                 'processed right now. Please try '
                                 'again later.'))
        return HttpResponse(content=e, status=400)



def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        print("DEBUG: Handling POST request")
        bag = request.session.get('bag', {})
        form_data = {
            'billing_full_name': request.POST['billing_full_name'],
            'billing_email': request.POST['billing_email'],
            'billing_phone_number': request.POST['billing_phone_number'],
            'billing_country': request.POST['billing_country'],
            'billing_postcode': request.POST['billing_postcode'],
            'billing_town_or_city': request.POST['billing_town_or_city'],
            'billing_street_address1': request.POST['billing_street_address1'],
            'billing_street_address2': request.POST['billing_street_address2'],
            'billing_county': request.POST['billing_county'],
        }

        order_form = OrderForm(form_data)
        print(f"DEBUG: Order form initialized: {order_form}")

        if order_form.is_valid():
            print("DEBUG: Order form is valid")
            order = order_form.save(commit=False)
            delivery_type = request.POST.get('order_type')  # Make sure this matches your form field

            if delivery_type == 'pickup':
                order.pick_up = True
                order.delivery_cost = settings.PICKUP_DELIVERY_PRICE
                messages.success(request, 'You have chosen to pick up your order from Coffee and Honey.')
            elif delivery_type == 'delivery-different':
                order.pick_up = False
                order.different_delivery_address = True
                # Use the form data to fill delivery fields
                order.delivery_name = order_form.cleaned_data['delivery_name']
                order.delivery_street_address1 = order_form.cleaned_data['delivery_street_address1']
                order.delivery_street_address2 = order_form.cleaned_data['delivery_street_address2']
                order.delivery_town_or_city = order_form.cleaned_data['delivery_town_or_city']
                order.delivery_county = order_form.cleaned_data['delivery_county']
                order.delivery_postcode = order_form.cleaned_data['delivery_postcode']
                order.delivery_country = order_form.cleaned_data['delivery_country']
                order.delivery_cost = calculate_delivery_cost(order.order_total)
            else:
                order.pick_up = False
                order.different_delivery_address = False
                # Copy billing address to delivery fields
                order.delivery_name = order.billing_full_name
                order.delivery_street_address1 = order.billing_street_address1
                order.delivery_street_address2 = order.billing_street_address2
                order.delivery_town_or_city = order.billing_town_or_city
                order.delivery_county = order.billing_county
                order.delivery_postcode = order.billing_postcode
                order.delivery_country = order.billing_country
                order.delivery_cost = calculate_delivery_cost(order.order_total)

            # Inspect the client secret
            print(f"DEBUG: Client secret from POST: {request.POST.get('client_secret')}")
            pid = request.POST.get('client_secret').split('_secret')[0]
            print(f"DEBUG: PID extracted: {pid}")

            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            order.save()
            print(f"DEBUG: Order saved: {order}")

            # Save the order line items, similar to previous logic
            for item_id, item_data in bag.items():
                try:
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        for size, size_data in item_data['items_by_size'].items():
                            quantity = size_data['quantity']
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_line_item.save()
                except Product.DoesNotExist:
                    print("DEBUG: Product.DoesNotExist error occurred")
                    messages.error(request, (
                        "One of the products in your bag wasn't "
                        "found in our database. "
                        "Please call us for assistance!"))
                    order.delete()
                    return redirect(reverse('view_bag'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            print("DEBUG: Order form is invalid")
            messages.error(request, 'There was an error with your form. Please double-check your information.')

    else:  # Handle GET requests
        print("DEBUG: Handling GET request")
        bag = request.session.get('bag', {})
        if not bag:
            print("DEBUG: Bag is empty")
            messages.error(request, "There's nothing in your bag at the moment")
            return redirect(reverse('products'))

        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        print(f"DEBUG: Stripe PaymentIntent created with amount: {stripe_total}")
        order_form = OrderForm()  # Initialize empty order form for GET requests

    if not stripe_public_key:
        print("DEBUG: Stripe public key missing")
        messages.warning(request, ('Stripe public key is missing. Did you forget to set it in your environment?'))

    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
        'delivery_price': settings.STANDARD_DELIVERY_PRICE,
        'pickup_price': settings.PICKUP_DELIVERY_PRICE,
    }

    print(f"DEBUG: Final context: {context}")
    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Attach the user's profile to the order
        order.user_profile = profile
        order.save()

        # Save the user's info
        if save_info:
            profile_data = {
                'default_phone_number': order.billing_phone_number,
                'default_country': order.billing_country,
                'default_postcode': order.billing_postcode,
                'default_town_or_city': order.billing_town_or_city,
                'default_street_address1': order.billing_street_address1,
                'default_street_address2': order.billing_street_address2,
                'default_county': order.billing_county,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.billing_email}.')

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)