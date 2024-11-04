from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['billing_full_name', 'billing_email', 'billing_phone_number',
                  'billing_street_address1', 'billing_street_address2',
                  'billing_town_or_city', 'billing_postcode',
                  'billing_country', 'billing_county',
                  # these are delivery address fields
                  'delivery_name', 'delivery_street_address1',
                  'delivery_street_address2',
                  'delivery_town_or_city', 'delivery_postcode',
                  'delivery_country',
                  'delivery_county']

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'billing_full_name': 'Full Name',
            'billing_email': 'Email Address',
            'billing_phone_number': 'Phone Number',
            'billing_postcode': 'Postal Code',
            'billing_town_or_city': 'Town or City',
            'billing_street_address1': 'Street Address 1',
            'billing_street_address2': 'Street Address 2',
            'billing_county': 'County, State, or Locality',
            'delivery_name': 'Recipient Name',
            'delivery_street_address1': 'Delivery Address 1',
            'delivery_street_address2': 'Delivery Address 2',
            'delivery_town_or_city': 'Delivery City or Town',
            'delivery_postcode': 'Delivery Postal Code',
            'delivery_country': 'Delivery Country',
            'delivery_county': 'Delivery County or Locality',
        }

        self.fields['billing_full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'billing_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
