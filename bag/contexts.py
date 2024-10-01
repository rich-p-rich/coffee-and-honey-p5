from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product, ProductVariant

def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    for item_id, item_data in bag.items():
        product = get_object_or_404(Product, pk=item_id)

        # Handling variants or no-variants cases
        if product.variants.exists():
            # Handle variant-specific logic
            if isinstance(item_data, int):
                variant = product.variants.first()
                if variant and variant.price:
                    total += item_data * variant.price
                    bag_items.append({
                        'item_id': item_id,
                        'quantity': item_data,
                        'product': product,
                        'variant': variant,
                    })
                else:
                    print(f"Error: No price found for variant {variant}")
            else:
                for size, quantity in item_data['items_by_size'].items():
                    variant = product.variants.get(weight=size)
                    if variant and variant.price:
                        total += quantity * variant.price
                        bag_items.append({
                            'item_id': item_id,
                            'quantity': quantity,
                            'product': product,
                            'variant': variant,
                            'size': size,
                        })
                    else:
                        print(f"Error: No price found for variant {variant}")
        else:
            # Handle products without variants
            if product.price:
                total += item_data * product.price
                bag_items.append({
                    'item_id': item_id,
                    'quantity': item_data,
                    'product': product,
                })
            else:
                print(f"Error: No price found for product {product.name}")

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = Decimal(settings.STANDARD_DELIVERY_PRICE)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = Decimal(0)
        free_delivery_delta = 0
    
    grand_total = delivery + total

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
