from django.db import models

# Create your models here.

class Category(models.Model):

    class Meta: 
        verbose_name_plural = 'Categories'
        
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def get_friendly_name(self):
        return self.friendly_name

class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  # For products without variants
    strength_rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)  # for the coffee
    extra_services = models.ManyToManyField('Service', blank=True)  # Allows multiple services: bean grinding and gift wrapping
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=4, decimal_places=0)  # Weight of the product
    price = models.DecimalField(max_digits=6, decimal_places=2)  # Price for this weight variant

    def __str__(self):
        return f"{self.product.name} - {self.weight}g" # g = grams

class Service(models.Model):
    name = models.CharField(max_length=254)
    description = models.TextField(null=True, blank=True)
    surcharge = models.DecimalField(max_digits=6, decimal_places=2)  # Additional costs for the added service

    def __str__(self):
        return self.name