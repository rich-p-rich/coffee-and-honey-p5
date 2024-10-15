import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings

from django_countries.fields import CountryField

from products.models import Product
from profiles.models import UserProfile

from decimal import Decimal


class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, 
                                        null=True, blank=True, related_name='orders')
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    pick_up = models.BooleanField(default=False) # Customer picks up the order in the cafe
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    original_bag = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')

    def set_delivery_cost(self):
        """
        Set delivery costs to 0 if customer choses to pick-up their order
        """
        if self.pick_up:
            self.delivery_cost = 0
        else:
            self.delivery_cost = calculate_delivery_cost(self.order_total)
        self.save()

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0

        # Ensure delivery cost is also a Decimal
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = Decimal(settings.STANDARD_DELIVERY_PRICE)
        else:
            self.delivery_cost = Decimal(0)

        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    product_size = models.CharField(max_length=7, null=True, blank=True)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        # Debugging print statements
        print(f"DEBUG: Product price type: {type(self.product.price)}")
        print(f"DEBUG: Product price value: {self.product.price}")
        print(f"DEBUG: Quantity type: {type(self.quantity)}")
        print(f"DEBUG: Quantity value: {self.quantity}")

        # Extract quantity from the dict if it's a dict
        if isinstance(self.quantity, dict):
            print("DEBUG: Extracting quantity from the dictionary")
            self.quantity = self.quantity.get('quantity', 1)  # Default to 1 if 'quantity' key is missing
        
        print(f"DEBUG: Corrected quantity: {self.quantity}")
        
        # If the product has variants, use the variant price
        if self.product.variants.exists():
            variant = self.product.variants.get(weight=self.product_size)
            print(f"DEBUG: Retrieved variant: {variant} with price: {variant.price}")
            self.lineitem_total = variant.price * self.quantity
        else:
            # Fallback to base product price if no variants
            if self.product.price is None:
                raise ValueError(f"Product {self.product} has no price set.")
            self.lineitem_total = self.product.price * self.quantity

        super().save(*args, **kwargs)


