from django.conf import settings
from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages 
from products.models import Product, ProductVariant, Service
from djmoney.models.fields import MoneyField
from django.http import Http404

# Create your views here.

def view_bag(request):
    """ A view that renders the bag contents page """

    bag = request.session.get('bag', {})
    bag_items = []
    total = 0
    print("Session data:", bag)

    for item_id, item_data in bag.items():
        product = get_object_or_404(Product, pk=item_id)

        # Check if the item has 'items_by_size' (for products with sizes)
        if isinstance(item_data, dict) and 'items_by_size' in item_data:
            for size, details in item_data['items_by_size'].items():
                variant = get_object_or_404(ProductVariant, product=product, weight=size)
                price = float(details['price'])
                quantity = details['quantity']
                extra_service_cost = details.get('extra_service_cost', 0)
                subtotal = (price * quantity) + extra_service_cost
                total += subtotal
                bag_items.append({
                    'product': product,
                    'item_id': item_id, 
                    'size': variant.weight,
                    'quantity': quantity,
                    'price': price,
                    'extra_service_cost': extra_service_cost,
                    'subtotal': subtotal
                })
        # Handle items without size (products that don't have size/weight variants)
        elif isinstance(item_data, dict):
            price = float(item_data['price'])
            quantity = item_data['quantity']
            extra_service_cost = item_data.get('extra_service_cost', 0)
            freshly_ground = item_data.get('freshly_ground', False)
            subtotal = price * quantity
            total += subtotal
            bag_items.append({
                'product': product,
                'item_id': item_id, 
                'quantity': quantity,
                'price': price,
                'extra_service_cost': extra_service_cost,
                'freshly_ground': freshly_ground,
                'subtotal': subtotal
            })
        else:
            # Handle items where item_data is an integer (i.e., just the quantity)
            quantity = item_data  # item_data is just the quantity here
            price = product.price if product.price else 0.0  # Use the base product price or set to 0.0 if None
            price = float(price)  # Convert price to float if not None
            subtotal = price * quantity
            total += subtotal
            bag_items.append({
                'product': product,
                'item_id': item_id, 
                'quantity': quantity,
                'price': price,
                'subtotal': subtotal
            })

    context = {
        'bag_items': bag_items,
        'total': total,
    }

    return render(request, 'bag/bag.html', context)


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    freshly_ground = request.POST.get('freshly_ground') == 'yes'
    redirect_url = request.POST.get('redirect_url')

    size = None
    price = None
    extra_service_cost = 0  # Initialize with a default value to avoid UnboundLocalError

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
        extra_service_cost = settings.FRESHLY_GROUND_BEANS * quantity
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
                    bag[item_id]['items_by_size'][size]['extra_service_cost'] += extra_service_cost
                    bag[item_id]['items_by_size'][size]['freshly_ground'] = freshly_ground
                    print(f"DEBUG: Updated bag item with size: {bag[item_id]['items_by_size'][size]}")  # Debug
                else:
                    bag[item_id]['items_by_size'][size] = {
                        'quantity': quantity,
                        'price': str(price),
                        'extra_service_cost': extra_service_cost,
                        'freshly_ground': freshly_ground,
                    }
                    print(f"DEBUG: New bag item with size: {bag[item_id]['items_by_size'][size]}")  # Debug
            else:
                bag[item_id]['items_by_size'] = {
                    size: {
                        'quantity': quantity,
                        'price': str(price),
                        'extra_service_cost': extra_service_cost,
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
                        'extra_service_cost': extra_service_cost,
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
    """ Adjust the quantity of the specified product to the shopping bag """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
            messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]}')
 
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
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)