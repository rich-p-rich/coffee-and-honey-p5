from django.conf import settings
from django.shortcuts import render, redirect, reverse
from django.shortcuts import HttpResponse, get_object_or_404
from django.contrib import messages
from products.models import Product, ProductVariant, Service
from djmoney.models.fields import MoneyField
from django.http import Http404
from decimal import Decimal


# Create your views here.

def view_bag(request):
    """ Render the bag contents page """
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    freshly_ground = request.POST.get('freshly_ground') == 'yes'
    redirect_url = request.POST.get('redirect_url')

    size = None
    price = None
    extra_service_cost = Decimal(0)  # Initialize as Decimal

    # Fetch the variant if a size is selected
    if 'product_size' in request.POST:
        size = request.POST['product_size']
        print("DEBUG: Selected size:", size)  # Debug
        try:
            variant = ProductVariant.objects.get(product=product, weight=size)
            price = variant.price
            print(f"DEBUG: Variant found - {variant} with price {price}")
        except ProductVariant.DoesNotExist:
            print(
                f"WARNING: No variant found for {product.name} in size {size}")
    else:
        price = product.price
        print(
            f"DEBUG: No size selected, using product base price: {price}")

    # Apply freshly_ground price (in settings) as flatrate
    if freshly_ground:
        extra_service_cost = Decimal(settings.FRESHLY_GROUND_BEANS)

    # Get the current shopping bag from the session
    bag = request.session.get('bag', {})

    # Handle products with sizes (variants)
    if size:
        if item_id in bag and isinstance(bag[item_id], dict):
            if 'items_by_size' in bag[item_id]:
                if size in bag[item_id]['items_by_size']:
                    bag[item_id]['items_by_size'][size]['quantity'] += quantity
                    bag[item_id]['items_by_size'][size][
                        'extra_service_cost'] = (
                     str(extra_service_cost)
                    )
                    bag[item_id]['items_by_size'][size][
                        'freshly_ground'] = freshly_ground
                else:
                    bag[item_id]['items_by_size'][size] = {
                        'quantity': quantity,
                        'price': str(price),
                        'extra_service_cost': str(extra_service_cost),
                        'freshly_ground': freshly_ground,
                    }
            else:
                bag[item_id]['items_by_size'] = {
                    size: {
                        'quantity': quantity,
                        'price': str(price),
                        'extra_service_cost': str(extra_service_cost),
                        'freshly_ground': freshly_ground,
                    }
                }
        else:
            bag[item_id] = {
                'items_by_size': {
                    size: {
                        'quantity': quantity,
                        'price': str(price),
                        'extra_service_cost': str(extra_service_cost),
                        'freshly_ground': freshly_ground,
                    }
                }
            }

    # Handle products without sizes
    else:
        if item_id in bag and isinstance(bag[item_id], dict):
            bag[item_id]['quantity'] += quantity
        elif item_id in bag:
            bag[item_id] += quantity
        else:
            bag[item_id] = {
                'quantity': quantity,
                'price': str(price),
            }
        print("DEBUG: Updated bag item without size:", bag[item_id])  # Debug

    # Update the session with the modified bag
    request.session['bag'] = bag
    request.session.modified = True  # Ensure session data is saved
    print("DEBUG: Final bag contents after update:", bag)  # Debug

    messages.success(request, f'Added {product.name} to your bag')

    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """ Adjust the quantity of the specified product in the shopping bag """
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = request.POST.get('product_size', None)
    freshly_ground = 'freshly_ground' in request.POST  # Check if extra service was selected originally
    bag = request.session.get('bag', {})

    # Retain existing size if only quantity is adjusted
    if not size and item_id in bag:
        size = list(bag[item_id]['items_by_size'].keys())[0]

    # Retrieve or calculate price based on the selected variant or base price
    try:
        variant = product.variants.get(weight=size)
        price = variant.price
    except ProductVariant.DoesNotExist:
        price = product.price  # Use base price if no variant found

    # Use the flat extra service cost from settings for the freshly ground option
    flat_service_cost = settings.FRESHLY_GROUND_BEANS if freshly_ground else 0

    # Update session bag data
    if quantity > 0:
        # If the item already exists in the bag, update all details, keeping service cost flat
        if item_id in bag and size in bag[item_id]['items_by_size']:
            item = bag[item_id]['items_by_size'][size]
            item['quantity'] = quantity
            item['price'] = str(price)
            item['total_extra_service_cost'] = str(flat_service_cost)  # Set flat rate from settings
            item['freshly_ground'] = freshly_ground
        else:
            # Add the new item with all details, including flat service cost
            bag[item_id] = {
                'items_by_size': {
                    size: {
                        'quantity': quantity,
                        'price': str(price),
                        'total_extra_service_cost': str(flat_service_cost),
                        'freshly_ground': freshly_ground,
                    }
                }
            }
        messages.success(request, f'Updated {product.name} quantity to {quantity}')
    else:
        # Remove the item if quantity is zero
        del bag[item_id]['items_by_size'][size]
        if not bag[item_id]['items_by_size']:  # Remove item if no sizes remain
            bag.pop(item_id)
        messages.success(request, f'Removed {product.name} from your bag')

    # Save updated bag data back to session
    request.session['bag'] = bag
    request.session.modified = True
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""

    try:
        product = get_object_or_404(Product, pk=item_id)
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(
                request,
                f'Removed size {size.upper()} {product.name} from your bag')
        else:
            bag.pop(item_id)
            messages.success(
             request, f'Removed {product.name} from your bag')

        request.session['bag'] = bag
        request.session.modified = True
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
