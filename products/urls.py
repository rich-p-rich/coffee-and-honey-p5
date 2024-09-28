from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='all_products'),  # Homepage with filtering functionality
    path('<int:product_id>/', views.product_detail, name='product_detail'),  # Detail page for each product
]

