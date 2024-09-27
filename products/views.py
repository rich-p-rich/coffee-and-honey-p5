from django.shortcuts import render
from .models import Category, Product, ProductVariant, Service


# Create your views here.

def all_products(request):
    """ A view to all products, plus sort and search queries"""

    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)