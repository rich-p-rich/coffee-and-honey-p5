from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, get_list_or_404, HttpResponse
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


def calculate_delivery_cost(delivery_type):
    """
    Calculate the delivery cost based on the order type using predefined settings.
    - Delivery to billing or recipient address costs STANDARD_DELIVERY_PRICE.
    - Pickup from cafe is free (PICKUP_DELIVERY_PRICE).
    """
    if delivery_type == "pickup":
        return settings.PICKUP_DELIVERY_PRICE
    return settings.STANDARD_DELIVERY_PRICE


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    # Always initialize stripe.api_key and intent
    stripe.api_key = stripe_secret_key
    intent = None

    if request.method == 'POST':
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

        if order_form.is_valid():
            order = order_form.save(commit=False)

            # Extract delivery type early on
            delivery_type = request.POST.get('delivery_type')

            # Set delivery cost based on the type
            order.delivery_cost = calculate_delivery_cost(delivery_type)

            # Handle each delivery type explicitly
            if delivery_type == 'pickup':
                order.pick_up = True
                order.different_delivery_address = False
                messages.success(request, 'You have chosen to pick up your order from Coffee and Honey.')
                order.save()

            elif delivery_type == 'delivery-different':
                order.pick_up = False
                order.different_delivery_address = True
                order.delivery_name = request.POST.get('delivery_name', order.billing_full_name)
                order.delivery_street_address1 = request.POST.get('delivery_street_address1')
                order.delivery_street_address2 = request.POST.get('delivery_street_address2', '')
                order.delivery_town_or_city = request.POST.get('delivery_town_or_city')
                order.delivery_county = request.POST.get('delivery_county', '')
                order.delivery_postcode = request.POST.get('delivery_postcode')
                order.delivery_country = request.POST.get('delivery_country')
                order.save()

            elif delivery_type == 'delivery-billing-same':
                order.pick_up = False
                order.different_delivery_address = False
                order.delivery_name = order.billing_full_name
                order.delivery_street_address1 = order.billing_street_address1
                order.delivery_street_address2 = order.billing_street_address2
                order.delivery_town_or_city = order.billing_town_or_city
                order.delivery_county = order.billing_county
                order.delivery_postcode = order.billing_postcode
                order.delivery_country = order.billing_country
                order.save()

            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            order.save()

            # Save each item in the bag as an OrderLineItem
            for item_id, item_data in bag.items():
                try:
                    product = Product.objects.get(id=item_id)
                    
                    if isinstance(item_data, int):
                        # Single-price product
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                            unit_price=product.price  # Set the unit price for single-price products
                        )
                        print(f"DEBUG: Product: {order_line_item.product.name}, Quantity: {order_line_item.quantity}, Unit Price: {order_line_item.unit_price}")
                        order_line_item.save()

                    else:
                        # Variant product
                        for size, data in item_data['items_by_size'].items():
                            quantity = int(data.get('quantity', 1))
                            variant = product.variants.get(weight=size)  # Fetch the variant
                            
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                                unit_price=variant.price  # Set the unit price for variant products
                            )
                            print(f"DEBUG: Product: {order_line_item.product.name}, Size: {order_line_item.product_size}, Quantity: {order_line_item.quantity}, Unit Price: {order_line_item.unit_price}")
                            order_line_item.save()

                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your bag wasn't "
                        "found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_bag'))


            # Now assign order totals using the bag contents context
            current_bag = bag_contents(request)
            order.order_total = current_bag['total']
            order.delivery_cost = current_bag['delivery']
            order.grand_total = current_bag['grand_total']
            order.save()

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))

        else:
            messages.error(request, 'There was an error with your form. Please double-check your information.')

    # Handle GET requests
    else:
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, "There's nothing in your bag at the moment")
            return redirect(reverse('products'))

        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        # Pre-fill form with default address from UserProfile if available
        user_profile = None
        initial_data = {}
        if request.user.is_authenticated:
            user_profile = request.user.userprofile
            initial_data = {
                'billing_full_name': user_profile.user.get_full_name(),
                'billing_email': user_profile.user.email,
                'billing_phone_number': user_profile.default_phone_number,
                'billing_street_address1': user_profile.default_street_address1,
                'billing_street_address2': user_profile.default_street_address2,
                'billing_town_or_city': user_profile.default_town_or_city,
                'billing_county': user_profile.default_county,
                'billing_postcode': user_profile.default_postcode,
                'billing_country': user_profile.default_country,
            }

        order_form = OrderForm(initial=initial_data)

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. Did you forget to set it in your environment?')

    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret if intent else '',
        'delivery_price': settings.STANDARD_DELIVERY_PRICE,
        'pickup_price': settings.PICKUP_DELIVERY_PRICE,
    }

    return render(request, 'checkout/checkout.html', context)



def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    # Fetch all line items for this order
    line_items = OrderLineItem.objects.filter(order=order)
    print(f"Line items count: {line_items.count()}")

    # Print the order details to verify them
    print(f"Order Pickup: {order.pick_up}")
    print(f"Order Different Delivery: {order.different_delivery_address}")
    print(f"Order Delivery Name: {order.delivery_name}")
    print(f"Order Delivery Address1: {order.delivery_street_address1}")

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

    # Clear the bag session
    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'line_items': line_items,
        'order_total': order.order_total,
        'delivery': order.delivery_cost,
        'grand_total': order.grand_total,
    }

    return render(request, template, context)