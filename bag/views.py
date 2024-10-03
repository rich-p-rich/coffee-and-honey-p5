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
    print("Session data:", bag)

    for item_id, item_data in bag.items():
        product = get_object_or_404(Product, pk=item_id)

        # Check if the item has 'items_by_size' (for products with sizes)
        if isinstance(item_data, dict) and 'items_by_size' in item_data:
            for size, details in item_data['items_by_size'].items():
                variant = get_object_or_404(ProductVariant, product=product, weight=size)
                price = float(details['price'])
                quantity = details['quantity']
                subtotal = price * quantity
                total += subtotal
                bag_items.append({
                    'product': product,
                    'size': variant.weight,
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

    # Print request.POST to see if 'product_size' is being posted
    print("POST data:", request.POST)

    size = None
    price = None

    # Fetch the variant if a size is selected
    if 'product_size' in request.POST:
        size = request.POST['product_size']
        variant = get_object_or_404(ProductVariant, product=product, weight=size)
        price = variant.price
    else:
        print("No size posted for this product.")

    # Get the current shopping bag from the session
    bag = request.session.get('bag', {})

    # Handle products with sizes (variants)
    if size:
        if item_id in bag and isinstance(bag[item_id], dict):
            if 'items_by_size' in bag[item_id]:
                if size in bag[item_id]['items_by_size']:
                    bag[item_id]['items_by_size'][size]['quantity'] += quantity
                else:
                    bag[item_id]['items_by_size'][size] = {'quantity': quantity, 'price': str(price)}
            else:
                bag[item_id]['items_by_size'] = {size: {'quantity': quantity, 'price': str(price)}}
        else:
            bag[item_id] = {'items_by_size': {size: {'quantity': quantity, 'price': str(price)}}}
    
    # Handle products without sizes
    else:
        if item_id in bag and isinstance(bag[item_id], dict):
            bag[item_id]['quantity'] += quantity
        elif item_id in bag:
            bag[item_id] += quantity
        else:
            bag[item_id] = {'quantity': quantity, 'price': str(product.price)}

    # Update the session with the modified bag
    request.session['bag'] = bag
    print("Bag after adding:", bag)  # Print the updated bag structure

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
