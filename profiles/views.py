from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

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
            print(f"DEBUG: Profile form saved. Data: {form.cleaned_data}")
            messages.success(request, 'Profile updated successfully')
        else:
            print("DEBUG: Profile form is invalid:", form.errors)

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
def set_billing_as_default(request):
    if request.method == 'POST':
        user_profile = request.user.userprofile
        # Ensure no other addresses are set as default
        RecipientAddresses.objects.filter(
             user_profile=user_profile, is_default=True
        ).update(is_default=False)
        # The billing address is now the default
        messages.success(
            request,
            "Your billing address is now your default shipping address."
        )
        return JsonResponse({"success": True}, status=200)
    return JsonResponse({"error": "Invalid request"}, status=400)


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
def add_address(request):
    """
    Add an address to the profile.
    """
    if request.method == 'POST':
        form = RecipientAddressesForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user_profile = request.user.userprofile
            address.save()
            messages.success(request, 'Address successfully added.')
            return redirect('saved_addresses')
    else:
        form = RecipientAddressesForm()

    context = {
        'form': form,
    }

    return render(request, 'profiles/add_address.html', context)


@login_required
def set_default_address(request, address_id):
    user_profile = request.user.userprofile
    address = get_object_or_404(
        RecipientAddresses,
        id=address_id,
        user_profile=user_profile
    )

    # Set all addresses to not be the default
    RecipientAddresses.objects.filter(
        user_profile=user_profile, is_default=True).update(is_default=False)

    # Set the selected address as the default
    address.is_default = True
    address.save()

    messages.success(request, "Default address has been updated.")
    return redirect('saved_addresses')


@login_required
def edit_address(request, address_id):
    """
    Edit a saved recipient address.
    """
    address = get_object_or_404(
        RecipientAddresses,
        id=address_id,
        user_profile=request.user.userprofile
    )

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
    if request.method == 'POST':
        address = get_object_or_404(
            RecipientAddresses,
            id=address_id,
            user_profile=request.user.userprofile
        )
        address.delete()
        messages.success(request, 'Recipient address deleted successfully.')
        return redirect('saved_addresses')
