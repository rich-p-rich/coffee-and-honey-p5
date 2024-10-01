from django.contrib import admin
from .models import Category, Product, ProductVariant, Service

class ProductVariantInline(admin.TabularInline):  
    model = ProductVariant
    extra = 1  

# Custom admin for Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'rating')  
    list_filter = ('category',)  
    search_fields = ('name', 'description')  
    inlines = [ProductVariantInline]  

# Custom admin for ProductVariant
@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'weight', 'price') 
    list_filter = ('product',)  
    search_fields = ('product__name',)  

# Custom admin for Service
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'surcharge')  
    search_fields = ('name',)  


admin.site.register(Category)
