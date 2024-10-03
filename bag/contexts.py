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
                for size, data in item_data['items_by_size'].items():
                    print(f"DEBUG: size={size}, quantity={data['quantity']}, item_data['items_by_size']={item_data['items_by_size']}")

                    quantity = data['quantity']

                    try:
                        variant = product.variants.get(weight=size)
                        print(f"DEBUG: Variant found: {variant}, Price: {variant.price}")

                        if variant and variant.price:
                            # Ensure price is handled as a Decimal
                            total += Decimal(quantity) * Decimal(variant.price)
                            print(f"DEBUG: Added {quantity} * {variant.price} to total: {total}")

                            bag_items.append({
                                'item_id': item_id,
                                'quantity': quantity,
                                'product': product,
                                'variant': variant,
                                'size': size,
                            })
                        else:
                            print(f"Error: No price found for variant {variant}")
                    except ProductVariant.DoesNotExist:
                        print(f"Error: No variant found for size {size}")
        else:
            # Handle products without variants
            print(f"DEBUG: {product.name} has no variants")
            if product.price:
                if isinstance(item_data, dict):
                    quantity = item_data.get('quantity', 1)

                else:
                    quantity = item_data

                total += Decimal(quantity) * Decimal(product.price)
                print(f"DEBUG: Added {quantity} * {product.price} to total: {total}")

                bag_items.append({
                    'item_id': item_id,
                    'quantity': item_data,
                    'product': product,
                })
            else:
                print(f"Error: No price found for product {product.name}")

    # Check to see if bag is empty before calculating delivery
    if total > 0:
        if total < settings.FREE_DELIVERY_THRESHOLD:
            delivery = Decimal(settings.STANDARD_DELIVERY_PRICE)
            free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
        else:
            delivery = Decimal(0)
            free_delivery_delta = 0
    else:
        delivery = Decimal(0)
        free_delivery_delta = 0

    grand_total = delivery + total
    print(f"DEBUG: Grand total: {grand_total}")

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    # Print the final context for confirmation
    print("DEBUG: Final bag context:", context)

    return context
