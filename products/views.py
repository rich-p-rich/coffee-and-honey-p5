from django.conf import settings
from django.shortcuts import render, get_object_or_404
from .models import Category, Product, ProductVariant, Service
from djmoney.models.fields import MoneyField

# All products plus filtering by category & name


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    category = request.GET.get('category', None)
    product_name = request.GET.get('name', None)

    if category:  # Filter by category
        products = Product.objects.filter(category__name__icontains=category)
    elif product_name:  # Filter by product
        products = Product.objects.filter(name__icontains=product_name)
    else:
        products = Product.objects.all()

    context = {
        'products': products,
        'selected_category': category,
        'selected_product_name': product_name,
    }

    return render(request, 'products/products.html', context)


# Product Detail Page
def product_detail(request, product_id):
    """ A view to display a single product, including any variants """
    product = get_object_or_404(Product, pk=product_id)

    # Check if the product has variants
    variants = product.variants.all() if product.variants.exists() else None

    context = {
        'product': product,
        'variants': variants,
        'freshly_ground_beans_price': settings.FRESHLY_GROUND_BEANS,
    }

    return render(request, 'products/product_detail.html', context)
