from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse
)
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order, OrderLineItem

from products.models import Product
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

    print("DEBUG: Starting checkout view")

    if request.method == 'POST':
        print("DEBUG: Handling POST request")
        bag = request.session.get('bag', {})
        print(f"DEBUG: Bag contents: {bag}")
        print(f"DEBUG: Bag data in session: {bag}")

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        
        # Add print statement to inspect form data
        print(f"DEBUG: POST form data: {form_data}")

        order_form = OrderForm(form_data)
        print(f"DEBUG: Order form initialized: {order_form}")

        if order_form.is_valid():
            print("DEBUG: Order form is valid")
            order = order_form.save(commit=False)

            if 'pick_up' in request.POST:
                order.pick_up = True
                # Confirmation message
                messages.success(request, 'You have selected to pick up your order in our cafe.')
            else:
                order.pick_up = False
            
            # Add print statement to inspect the client secret
            print(f"DEBUG: Client secret from POST: {request.POST.get('client_secret')}")

            pid = request.POST.get('client_secret').split('_secret')[0]
            
            # Add print statement to inspect the extracted PID
            print(f"DEBUG: PID extracted: {pid}")

            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            order.save()
            print(f"DEBUG: Order saved: {order}")

            for item_id, item_data in bag.items():
                try:
                    product = Product.objects.get(id=item_id)
                    print(f"DEBUG: Product found: {product}")

                    if isinstance(item_data, int):
                        # Handling products without sizes (simple products)
                        print(f"DEBUG: Item data is an integer: {item_data}")
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,  # Quantity is already an integer here
                        )
                        order_line_item.save()
                        print(f"DEBUG: Order line item saved: {order_line_item}")
                    else:
                        # Handling products with sizes (variants)
                        print(f"DEBUG: Item data contains sizes: {item_data['items_by_size']}")
                        for size, size_data in item_data['items_by_size'].items():
                            quantity = size_data['quantity']  # Extract just the quantity from the dictionary
                            price = size_data['price']  # (Optional) Extract price if needed
                            print(f"DEBUG: Correct quantity: {quantity}, Price: {price}")

                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,  # Now using the extracted quantity
                                product_size=size,  # Size of the product
                            )
                            order_line_item.save()
                            print(f"DEBUG: Order line item saved: {order_line_item}")

                except Product.DoesNotExist:
                    print("DEBUG: Product.DoesNotExist error occurred")
                    messages.error(request, (
                        "One of the products in your bag wasn't "
                        "found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()
                    print("DEBUG: Order deleted")
                    return redirect(reverse('view_bag'))

            # Save the info to the user's profile if all is well
            request.session['save_info'] = 'save-info' in request.POST
            print("DEBUG: Redirecting to checkout_success")
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            print("DEBUG: Order form is invalid")
            messages.error(request, ('There was an error with your form. '
                                     'Please double check your information.'))
    else:
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

        # Initialize an empty order form for GET requests
        order_form = OrderForm()

    if not stripe_public_key:
        print("DEBUG: Stripe public key missing")
        messages.warning(request, ('Stripe public key is missing. '
                                   'Did you forget to set it in '
                                   'your environment?'))

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    print(f"DEBUG: Final context: {context}")
    return render(request, template, context)


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
                'default_phone_number': order.phone_number,
                'default_country': order.country,
                'default_postcode': order.postcode,
                'default_town_or_city': order.town_or_city,
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_county': order.county,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)