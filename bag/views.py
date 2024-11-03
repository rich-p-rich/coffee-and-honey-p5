from django.conf import settings
from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
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
    extra_service_cost = Decimal(0)  # Initialize as Decimal to avoid UnboundLocalError

    print("DEBUG: Starting add_to_bag")
    print("DEBUG: Freshly Ground:", freshly_ground)  # Debug

    # Fetch the variant if a size is selected
    if 'product_size' in request.POST:
        size = request.POST['product_size']
        print("DEBUG: Selected size:", size)  # Debug
        try:
            variant = ProductVariant.objects.get(product=product, weight=size)
            price = variant.price
            print(f"DEBUG: Variant found - {variant} with price {price}")  # Debug
        except ProductVariant.DoesNotExist:
            print(f"WARNING: No variant found for product {product.name} with size {size}")
    else:
        price = product.price
        print(f"DEBUG: No size selected, using product base price: {price}")

    # Calculate the total extra service cost based on quantity if 'freshly_ground' is selected
    if freshly_ground and size:  # Only calculate extra service if a size is selected
        extra_service_cost = Decimal(settings.FRESHLY_GROUND_BEANS) * Decimal(quantity)
    print("DEBUG: Extra Service Cost after calculation:", extra_service_cost)  # Debug

    # Get the current shopping bag from the session
    bag = request.session.get('bag', {})
    print("DEBUG: Initial bag contents:", bag)

    # Handle products with sizes (variants)
    if size:
        if item_id in bag and isinstance(bag[item_id], dict):
            if 'items_by_size' in bag[item_id]:
                if size in bag[item_id]['items_by_size']:
                    bag[item_id]['items_by_size'][size]['quantity'] += quantity
                    bag[item_id]['items_by_size'][size]['extra_service_cost'] = str(extra_service_cost)  # Store as string
                    bag[item_id]['items_by_size'][size]['freshly_ground'] = freshly_ground
                    print(f"DEBUG: Updated bag item with size: {bag[item_id]['items_by_size'][size]}")  # Debug
                else:
                    bag[item_id]['items_by_size'][size] = {
                        'quantity': quantity,
                        'price': str(price),
                        'extra_service_cost': str(extra_service_cost),  # Store as string
                        'freshly_ground': freshly_ground,
                    }
                    print(f"DEBUG: New bag item with size: {bag[item_id]['items_by_size'][size]}")  # Debug
            else:
                bag[item_id]['items_by_size'] = {
                    size: {
                        'quantity': quantity,
                        'price': str(price),
                        'extra_service_cost': str(extra_service_cost),  # Store as string
                        'freshly_ground': freshly_ground,
                    }
                }
                print(f"DEBUG: Created items_by_size: {bag[item_id]['items_by_size']}")  # Debug
        else:
            bag[item_id] = {
                'items_by_size': {
                    size: {
                        'quantity': quantity,
                        'price': str(price),
                        'extra_service_cost': str(extra_service_cost),  # Store as string
                        'freshly_ground': freshly_ground,
                    }
                }
            }
            print(f"DEBUG: Added new item to bag with size: {bag[item_id]}")  # Debug

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
    size = request.POST.get('product_size', None)  # Fetch size from POST data
    freshly_ground = 'freshly_ground' in request.POST  # Check if the extra service is selected
    bag = request.session.get('bag', {})

    # Retain existing size if only quantity is adjusted
    if not size and item_id in bag:
        # Keep the original size if no new size was specified
        size = list(bag[item_id]['items_by_size'].keys())[0]

    try:
        # Look for the variant with the specified size
        variant = product.variants.get(weight=size)
        price = variant.price
    except ProductVariant.DoesNotExist:
        price = product.price  # Default to base price if variant not found

    # Retrieve the existing extra service cost, if available
    extra_service_cost = request.POST.get(
        'extra_service_cost', 
        bag[item_id]['items_by_size'][size].get('extra_service_cost', '0')
    )

    # Update session bag data
    if quantity > 0:
        # Update or add the item with the selected size and service
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

    """ Adjust the quantity of the specified product to the shopping bag """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        # Retrieve the variant price if available, fallback to product price
        try:
            variant = product.variants.get(weight=size)
            price = variant.price if variant and variant.price else product.price
        except ProductVariant.DoesNotExist:
            price = product.price  # Use product base price if no variant is found

        if quantity > 0:
            bag[item_id]['items_by_size'][size] = {
                'quantity': quantity,
                'price': str(price),  # Convert to string for session storage
                'extra_service_cost': str(extra_service_cost) if 'extra_service_cost' in bag[item_id]['items_by_size'][size] else '0',
                'freshly_ground': freshly_ground if 'freshly_ground' in bag[item_id]['items_by_size'][size] else False
            }
        else:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(request, f'Removed size {size.upper()} {product.name} from your bag')

    else:
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag') 

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
            messages.success(request, f'Removed size {size.upper()} {product.name} from your bag')
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

        request.session['bag'] = bag
        request.session.modified = True
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)