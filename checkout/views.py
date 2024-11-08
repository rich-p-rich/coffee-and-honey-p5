from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, get_list_or_404, HttpResponse
)
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order, OrderLineItem

from products.models import Product, ProductVariant
from profiles.models import RecipientAddresses
from profiles.forms import UserProfileForm
from profiles.models import UserProfile
from bag.contexts import bag_contents

from decimal import Decimal

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


def calculate_grand_total(order_total, delivery_cost):
    """Calculate and return the grand total."""
    return order_total + delivery_cost


def get_order_form_data(request):
    """Extract and return form data from the request for creating an order."""
    return {
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


def set_delivery_cost(order, delivery_type, request):
    """Set the delivery cost based on the delivery type."""
    if delivery_type == 'pickup':
        order.delivery_cost = settings.PICKUP_DELIVERY_PRICE
        order.pick_up = True
        order.different_delivery_address = False
        messages.success(request, 'You have chosen to pick up your order from Coffee and Honey.')
    else:
        order.delivery_cost = settings.STANDARD_DELIVERY_PRICE
        order.pick_up = False
        if delivery_type == 'delivery-different':
            order.different_delivery_address = True
        else:
            order.different_delivery_address = False


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    stripe.api_key = stripe_secret_key
    intent = None

    if request.method == 'POST':
        bag = request.session.get('bag', {})
        form_data = get_order_form_data(request)
        order_form = OrderForm(form_data)

        if order_form.is_valid():
            order = order_form.save(commit=False)

            # Set user profile if user is authenticated
            if request.user.is_authenticated:
                order.user_profile = request.user.userprofile

            # Determine delivery type and set delivery cost
            delivery_type = request.POST.get('delivery_type')
            set_delivery_cost(order, delivery_type, request)

            # Calculate totals
            current_bag = bag_contents(request)
            order.order_total = Decimal(current_bag['total'])
            order.grand_total = order.order_total + order.delivery_cost
            print(f"[DEBUG] Order Total: {order.order_total}")
            print(f"[DEBUG] Delivery Cost: {order.delivery_cost}")
            print(f"[DEBUG] Grand Total (Order): {order.grand_total}")
            order.save()

            # Stripe payment intent based on grand total
            stripe_total = round(order.grand_total * 100)
            print(f"[DEBUG] Stripe Total (Amount to be Charged): {stripe_total}")
            intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency=settings.STRIPE_CURRENCY,
            )

            # Process each item in the bag
            for item_id, item_data in bag.items():
                try:
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        OrderLineItem.objects.create(
                            order=order,
                            product=product,
                            quantity=item_data,
                            unit_price=product.price
                        )
                    else:
                        for size, data in item_data['items_by_size'].items():
                            variant = product.variants.get(weight=size)
                            OrderLineItem.objects.create(
                                order=order,
                                product=product,
                                quantity=int(data['quantity']),
                                product_size=size,
                                unit_price=variant.price
                            )
                except Product.DoesNotExist:
                    messages.error(request, "One of the products in your bag wasn't found in our database. Please call us for assistance!")
                    order.delete()
                    return redirect(reverse('view_bag'))

            # Redirect to success page
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))

        else:
            messages.error(request, 'Please check the errors in your form.')

    else:  # GET request handling
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, "There's nothing in your bag at the moment")
            return redirect(reverse('products'))

        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        print(f"[DEBUG] Grand Total from Bag (for GET request): {total}")
        
        # Use grand_total from order calculations to create payment intent
        stripe_total = round(total * 100)
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        # Prepare order form and context data
        user_profile = None
        initial_data = {}
        saved_addresses = None
        delivery_initial_data = {}

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

            saved_addresses = RecipientAddresses.objects.filter(user_profile=user_profile)
            default_delivery_address = saved_addresses.filter(is_default=True).first()
            if default_delivery_address:
                delivery_initial_data = {
                    'delivery_name': default_delivery_address.recipient_name,
                    'delivery_phone_number': default_delivery_address.recipient_phone_number,
                    'delivery_street_address1': default_delivery_address.recipient_street_address1,
                    'delivery_street_address2': default_delivery_address.recipient_street_address2,
                    'delivery_town_or_city': default_delivery_address.recipient_town_or_city,
                    'delivery_county': default_delivery_address.recipient_county,
                    'delivery_postcode': default_delivery_address.recipient_postcode,
                    'delivery_country': default_delivery_address.recipient_country,
                }

        order_form = OrderForm(initial={**initial_data, **delivery_initial_data})
        
        print(f"Order Total: {total if 'total' in locals() else 0.00}, "
                f"Delivery Cost: {delivery if 'delivery' in locals() else 0.00}, "
                f"Grand Total: {grand_total if 'grand_total' in locals() else 0.00}")

        context = {
            'order_form': order_form,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret if intent else '',
            'delivery_price': settings.STANDARD_DELIVERY_PRICE,
            'pickup_price': settings.PICKUP_DELIVERY_PRICE,
            'saved_addresses': saved_addresses,
            'default_delivery_data': delivery_initial_data,
        }

        return render(request, 'checkout/checkout.html', context)



def checkout_success(request, order_number):
    """Handle successful checkouts"""
    order = get_object_or_404(Order, order_number=order_number)

    # Retrieve bag from session
    bag = request.session.get('bag', {})
    line_items = []  # Initialize an empty list for line items

    # Process each item in the bag
    for item_id, item_data in bag.items():
        product = get_object_or_404(Product, pk=item_id)

        # Check if the item has 'items_by_size' (products with weight/price)
        if isinstance(item_data, dict) and 'items_by_size' in item_data:
            for size, details in item_data['items_by_size'].items():
                # Fetch the specific variant based on product and weight (size)
                variant = get_object_or_404(
                    ProductVariant, product=product, weight=size)
                price = float(details.get('price', 0))
                quantity = int(details.get('quantity', 1))
                extra_service_cost = float(details.get(
                    'extra_service_cost', 0))
                subtotal = (price * quantity) + extra_service_cost

                # Append item details to line_items
                line_items.append({
                    'product': product,
                    'product_size': variant.weight,
                    'quantity': quantity,
                    'unit_price': price,
                    'extra_service_cost': extra_service_cost,
                    'subtotal': subtotal,
                })
        else:
            # For items without sizes / *no* weight/price variations
            price = float(item_data.get('price', 0))
            quantity = int(item_data.get('quantity', 1))
            extra_service_cost = float(item_data.get('extra_service_cost', 0))
            subtotal = (price * quantity) + extra_service_cost

            line_items.append({
                'product': product,
                'quantity': quantity,
                'unit_price': price,
                'extra_service_cost': extra_service_cost,
                'subtotal': subtotal,
            })

    context = {
        'order': order,
        'line_items': line_items,
        'delivery': order.delivery_cost,
        'grand_total': order.grand_total,
    }

    # Clear the session bag as the order is complete
    request.session['bag'] = {}
    return render(request, 'checkout/checkout_success.html', context)