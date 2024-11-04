from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product, ProductVariant


def bag_contents(request):
    bag_items = []
    total = Decimal(0)  # Initialize total as Decimal
    product_count = 0
    bag = request.session.get('bag', {})

    for item_id, item_data in bag.items():
        product = get_object_or_404(Product, pk=item_id)
        variant = None

        if product.variants.exists():
            # Handle variant-specific logic
            if isinstance(item_data, int):
                # Fallback case if item_data is an integer
                variant = product.variants.first()
                if variant and variant.price:
                    item_subtotal = Decimal(variant.price) * Decimal(item_data)
                    total += item_subtotal
                    product_count += item_data
                    bag_items.append({
                        'item_id': item_id,
                        'quantity': item_data,
                        'product': product,
                        'variant': variant,
                        'item_subtotal': item_subtotal,
                    })
                else:
                    print(f"Warning: No price found for variant {variant}")
            else:
                # Handle structured data with 'items_by_size'
                for size, data in item_data.get('items_by_size', {}).items():
                    quantity = data.get('quantity', 1)
                    price = Decimal(data.get(
                        'price', variant.price if variant else product.price))
                    extra_service_cost = Decimal(
                        data.get('extra_service_cost', 0))
                    freshly_ground = data.get('freshly_ground', False)

                    try:
                        variant = product.variants.get(weight=size)
                        if variant and variant.price:
                            # Calculate item and service subtotals
                            item_subtotal = (
                                Decimal(variant.price) * Decimal(quantity)
                            )
                            service_subtotal = extra_service_cost
                            total += item_subtotal + service_subtotal
                            product_count += quantity
                            bag_items.append({
                                'item_id': item_id,
                                'quantity': quantity,
                                'product': product,
                                'variant': variant,
                                'size': size,
                                'extra_service_cost': extra_service_cost,
                                'freshly_ground': freshly_ground,
                                'item_subtotal': item_subtotal,
                                'service_subtotal': service_subtotal,
                            })
                        else:
                            print(
                              f"Warning: No price found for variant {variant}")
                    except ProductVariant.DoesNotExist:
                        print(f"Warning: No variant found for size {size}")

        else:
            # Handle products without variants
            quantity = item_data.get('quantity', 1) if isinstance(
                item_data, dict) else item_data

            if product.price:
                item_subtotal = Decimal(product.price) * Decimal(quantity)
                total += item_subtotal
                product_count += quantity
                bag_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': product,
                    'item_subtotal': item_subtotal,
                })
            else:
                print(f"Warning: No price found for product {product.name}")

    # Delivery cost (a free shipping conditional could be added here)
    delivery = Decimal(settings.STANDARD_DELIVERY_PRICE)

    # Calculate grand total
    grand_total = total + delivery

    # Context including the delivery and grand total
    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'grand_total': grand_total,
    }

    return context
