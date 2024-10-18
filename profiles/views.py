from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile, RecipientAddresses
from .forms import UserProfileForm, RecipientAddressesForm

from checkout.models import Order

@login_required
def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')

    form = UserProfileForm(instance=profile)
    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True
    }

    return render(request, template, context)

@login_required
def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)

@login_required
def saved_addresses(request):
    """
    - View all recipient addresses saved to the user's profile
    - Save a new recipient address to the user's profile
    """
    user_profile = request.user.userprofile
    
    if request.method == 'POST':
        form = RecipientAddressesForm(request.POST)
        if form.is_valid():
            recipient_address = form.save(commit=False)
            recipient_address.user_profile = user_profile
            recipient_address.save()
            messages.success(request, 'New address added successfully.')
            return redirect('saved_addresses')
    else:
        form = RecipientAddressesForm()

    # Display all saved addresses
    addresses = RecipientAddresses.objects.filter(user_profile=user_profile)

    context = {
        'form': form,
        'addresses': addresses,
    }
    
    return render(request, 'profiles/saved_addresses.html', context)

@login_required
def edit_address(request, address_id):
    """
    Edit a saved recipient address.
    """
    address = get_object_or_404(RecipientAddresses, id=address_id, user_profile=request.user.userprofile)
    
    if request.method == 'POST':
        form = RecipientAddressesForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address successfully updated.')
            return redirect('saved_addresses')
    else:
        form = RecipientAddressesForm(instance=address)
    
    context = {
        'form': form,
        'address': address,
    }
    
    return render(request, 'profiles/edit_address.html', context)

@login_required
def delete_address(request, address_id):
    """
    Delete a saved recipient address.
    """
    address = get_object_or_404(RecipientAddresses, id=address_id, user_profile=request.user.userprofile)
    address.delete()
    messages.success(request, 'Recipient address deleted successfully.')
    return redirect('saved_addresses')