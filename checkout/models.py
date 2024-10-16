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
    billing_full_name = models.CharField(max_length=50, null=False, blank=False)
    billing_email = models.EmailField(max_length=254, null=False, blank=False)
    billing_phone_number = models.CharField(max_length=20, null=False, blank=False)
    billing_country = CountryField(blank_label='Country *', null=False, blank=False)
    billing_postcode = models.CharField(max_length=20, null=True, blank=True)
    billing_town_or_city = models.CharField(max_length=40, null=False, blank=False)
    billing_street_address1 = models.CharField(max_length=80, null=False, blank=False)
    billing_street_address2 = models.CharField(max_length=80, null=True, blank=True)
    billing_county = models.CharField(max_length=80, null=True, blank=True)
    different_delivery_address = models.BooleanField(default=False) # Default is billing address == shipping address
    pick_up = models.BooleanField(default=False) # Customer can choose to pick up the order in the cafe rather than have it shipped
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
        # If customer chooses pick-up, delivery_cost will be set to 0 in delivery_options
    date = models.DateTimeField(auto_now_add=True)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    original_bag = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')

    def delivery_options(self, form=None, user=None):
        """
        Define delivery / pick-up options and set delivery costs
        """
        if self.pick_up:
            # If the customer chooses to pick up in the cafe, set delivery cost to 0
            self.delivery_cost = 0

        elif self.different_delivery_address:
            # If customer want to ship to a saved address in their profile
            if user and user.profile.saved_addresses.exists():
                saved_address = user.profile.saved_addresses.last()  # Or use another selection logic
                self.copy_address(
                    saved_address.name,
                    saved_address.street_address1,
                    saved_address.street_address2,
                    saved_address.town_or_city,
                    saved_address.county,
                    saved_address.postcode,
                    saved_address.country
                )
            # If customer is entering a new / unsaved delivery address
            elif form:
                self.copy_address(
                    form.cleaned_data['delivery_name'],
                    form.cleaned_data['delivery_street_address1'],
                    form.cleaned_data['delivery_street_address2'],
                    form.cleaned_data['delivery_town_or_city'],
                    form.cleaned_data['delivery_county'],
                    form.cleaned_data['delivery_postcode'],
                    form.cleaned_data['delivery_country']
                )
            self.delivery_cost = calculate_delivery_cost(self.order_total)

        else:
            # If billing address == delivery address, copy billing address to delivery fields
            self.copy_address(
                self.billing_full_name,
                self.billing_street_address1,
                self.billing_street_address2,
                self.billing_town_or_city,
                self.billing_county,
                self.billing_postcode,
                self.billing_country
            )
            self.delivery_cost = calculate_delivery_cost(self.order_total)
        
        self.save()


    def copy_address(self, name, street1, street2, town, county, postcode, country):
        """
        Helper method to copy address fields to delivery address fields
        """
        self.delivery_name = name
        self.delivery_street_address1 = street1
        self.delivery_street_address2 = street2
        self.delivery_town_or_city = town
        self.delivery_county = county
        self.delivery_postcode = postcode
        self.delivery_country = country

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

        # Ensure delivery cost is also a decimal
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


