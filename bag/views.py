from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages 
from products.models import Product, ProductVariant, Service
from djmoney.models.fields import MoneyField

# Create your views here.

def view_bag(request):
    """ A view that renders the bag contents page """

    bag = request.session.get('bag', {})
    bag_items = []
    total = 0

    for item_id, item_data in bag.items():
        product = get_object_or_404(Product, pk=item_id)

        # Check if the item has 'items_by_size' (for products with sizes)
        if isinstance(item_data, dict) and 'items_by_size' in item_data:
            for size, details in item_data['items_by_size'].items():
                price = float(details['price'])
                quantity = details['quantity']
                subtotal = price * quantity
                total += subtotal
                bag_items.append({
                    'product': product,
                    'size': size,
                    'quantity': quantity,
                    'price': price,
                    'subtotal': subtotal
                })
        # Handle items without size (like products that don't have variants)
        elif isinstance(item_data, dict):
            price = float(item_data['price'])
            quantity = item_data['quantity']
            subtotal = price * quantity
            total += subtotal
            bag_items.append({
                'product': product,
                'quantity': quantity,
                'price': price,
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
    redirect_url = request.POST.get('redirect_url')
    size = None
    price = None  # Add price variable

    if 'product_size' in request.POST:
        size = request.POST['product_size']
        # Fetch the correct variant based on the size
        variant = get_object_or_404(ProductVariant, product=product, weight=size)
        price = variant.price

    bag = request.session.get('bag', {})

    if size:
        if item_id in list(bag.keys()):
            if isinstance(bag[item_id], dict):  # Check if the item is stored as a dictionary
                if size in bag[item_id]['items_by_size'].keys():
                    bag[item_id]['items_by_size'][size]['quantity'] += quantity
                    messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]["quantity"]}')
                else:
                    bag[item_id]['items_by_size'][size] = {'quantity': quantity, 'price': str(price)}  # Store price in the session
                    messages.success(request, f'Added size {size.upper()} {product.name} to your bag')
            else:
                # If bag[item_id] is not a dict, replace it with a dict to handle sizes
                bag[item_id] = {'items_by_size': {size: {'quantity': quantity, 'price': str(price)}}}
                messages.success(request, f'Added size {size.upper()} {product.name} to your bag')
        else:
            bag[item_id] = {'items_by_size': {size: {'quantity': quantity, 'price': str(price)}}}
            messages.success(request, f'Added size {size.upper()} {product.name} to your bag')
    else:
        if item_id in list(bag.keys()):
            if isinstance(bag[item_id], dict):
                # If it's a dict, update the quantity without size
                bag[item_id]['quantity'] += quantity
            else:
                # If it's an int, just update the quantity
                bag[item_id] += quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
            # Handle non-size items by adding just the quantity
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag')

    request.session['bag'] = bag
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
