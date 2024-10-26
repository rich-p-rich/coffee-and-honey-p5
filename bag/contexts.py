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
                # Fallback case if item_data is an integer
                variant = product.variants.first()
                if variant and variant.price:
                    total += item_data * variant.price
                    product_count += item_data
                    bag_items.append({
                        'item_id': item_id,
                        'quantity': item_data,
                        'product': product,
                        'variant': variant,
                        'subtotal': Decimal(variant.price) * Decimal(item_data),
                    })
                else:
                    print(f"Warning: No price found for variant {variant}")
            else:
                # Handle structured data with 'items_by_size'
                for size, data in item_data.get('items_by_size', {}).items():
                    quantity = data.get('quantity', 1)

                    try:
                        variant = product.variants.get(weight=size)
                        if variant and variant.price:
                            total += Decimal(quantity) * Decimal(variant.price)
                            product_count += quantity
                            bag_items.append({
                                'item_id': item_id,
                                'quantity': quantity,
                                'product': product,
                                'variant': variant,
                                'size': size,
                                'subtotal': Decimal(variant.price) * Decimal(quantity),
                            })
                        else:
                            print(f"Warning: No price found for variant {variant}")
                    except ProductVariant.DoesNotExist:
                        print(f"Warning: No variant found for size {size}")
        else:
            # Handle products without variants
            quantity = item_data.get('quantity', 1) if isinstance(item_data, dict) else item_data

            if product.price:
                total += Decimal(quantity) * Decimal(product.price)
                product_count += quantity
                bag_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': product,
                    'subtotal': Decimal(product.price) * Decimal(quantity),
                })
            else:
                print(f"Warning: No price found for product {product.name}")

    # Calculate delivery cost based on the total
    delivery = Decimal(settings.STANDARD_DELIVERY_PRICE) if total > 0 else Decimal(0)
    grand_total = delivery + total

    # Context including the delivery and grand total
    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'grand_total': grand_total,
    }

    # Print the final context for confirmation
    print("DEBUG: Final bag context:", context)

    return context
