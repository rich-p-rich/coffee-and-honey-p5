from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_countries.fields import CountryField


class UserProfile(models.Model):
    """
    A user profile model for maintaining default
    delivery information and order history
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_phone_number = models.CharField(max_length=20, null=True, blank=True)
    default_street_address1 = models.CharField(max_length=80, null=True, blank=True)
    default_street_address2 = models.CharField(max_length=80, null=True, blank=True)
    default_town_or_city = models.CharField(max_length=40, null=True, blank=True)
    default_county = models.CharField(max_length=80, null=True, blank=True)
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    default_country = models.CharField(max_length=40, null=True, blank=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.userprofile.save()
    
class RecipientAddresses(models.Model):
    """
    This saved additional delivery addresses in the user's profile for shipping
    to family, friends, etc 
    """
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='saved_addresses')
    recipient_name = models.CharField(max_length=50)
    recipient_phone_number = models.CharField(max_length=20, null=True, blank=True)
    recipient_street_address1 = models.CharField(max_length=80)
    recipient_street_address2 = models.CharField(max_length=80, null=True, blank=True)
    recipient_town_or_city = models.CharField(max_length=40)
    recipient_county = models.CharField(max_length=80, null=True, blank=True)
    recipient_postcode = models.CharField(max_length=20, null=True, blank=True)
    recipient_country = models.CharField(max_length=40, null=True, blank=True)
    nickname = models.CharField(max_length=50, blank=True, help_text="Nickname for this address (e.g., 'Mum and Dad', 'The Office', etc)")
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.street_address1}, {self.town_or_city}"
        return self.nickname or self.recipient_name  # Fallback if no nickname is provided