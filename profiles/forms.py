from django import forms
from .models import UserProfile, RecipientAddresses


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_country': 'Country',
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_county': 'County, State or Locality',
        }

        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:  
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder  
            self.fields[field].widget.attrs['class'] = 'border-black rounded-0 profile-form-input'
            self.fields[field].label = False

class RecipientAddressesForm(forms.ModelForm):
    class Meta:
        model = RecipientAddresses
        fields = [
            'recipient_name', 
            'recipient_street_address1', 
            'recipient_street_address2',
            'recipient_town_or_city', 
            'recipient_county', 
            'recipient_postcode', 
            'recipient_country'
        ]
       
    def __init__(self, *args, **kwargs):
        """
        Add placeholders for storing the reicipient's shipping details
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'recipient_name': 'Recipient Name',
            'recipient_street_address1': 'Street Address 1',
            'recipient_street_address2': 'Street Address 2',
            'recipient_town_or_city': 'Town or City',
            'recipient_county': 'County, State or Locality',
            'recipient_postcode': 'Postal Code',
            'recipient_country': 'Country',
        }

        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:  
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder  
            self.fields[field].widget.attrs['class'] = 'border-black rounded-0 profile-form-input'
            self.fields[field].label = False