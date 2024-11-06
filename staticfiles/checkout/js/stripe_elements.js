/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment

    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();
var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};
var card = elements.create('card', {style: style});
card.mount('#card-element');

// Handle realtime validation errors on the card element
card.addEventListener('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

// Handle form submit
var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
    ev.preventDefault();
    card.update({ 'disabled': true});
    $('#submit-button').attr('disabled', true);
    $('#payment-form').fadeToggle(100);
    $('#loading-overlay').fadeToggle(100);

    var saveInfo = Boolean($('#id-save-info').attr('checked'));
    // From using {% csrf_token %} in the form
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var postData = {
        'csrfmiddlewaretoken': csrfToken,
        'client_secret': clientSecret,
        'save_info': saveInfo,
    };
    var url = '/checkout/cache_checkout_data/';

    $.post(url, postData).done(function () {
        const isPickup = $('#pickup').is(':checked'); // For pick-up in cafe
        const isDifferentDelivery = $('#different-delivery-address').is(':checked'); // For different delivery address
    
        let billingDetails = {
            name: $.trim(form.billing_full_name.value),
            phone: $.trim(form.billing_phone_number.value),
            email: $.trim(form.billing_email.value),
            address: {
                line1: $.trim(form.billing_street_address1.value),
                line2: $.trim(form.billing_street_address2.value),
                city: $.trim(form.billing_town_or_city.value),
                country: $.trim(form.billing_country.value),
                state: $.trim(form.billing_county.value),
                postal_code: $.trim(form.billing_postcode.value)
            }
        };
    
        let shippingDetails;
    
        if (isPickup) {
            // If the order is for pickup, we do not need to provide shipping details.
            shippingDetails = null;
        } else if (isDifferentDelivery) {
            // If the customer is using a different delivery address, get those fields
            shippingDetails = {
                name: $.trim(form.delivery_name.value),
                phone: $.trim(form.delivery_phone_number.value), // Add this field to your form if necessary
                address: {
                    line1: $.trim(form.delivery_street_address1.value),
                    line2: $.trim(form.delivery_street_address2.value),
                    city: $.trim(form.delivery_town_or_city.value),
                    country: $.trim(form.delivery_country.value),
                    postal_code: $.trim(form.delivery_postcode.value),
                    state: $.trim(form.delivery_county.value)
                }
            };
        } else {
            // If the delivery address is the same as the billing address
            shippingDetails = {
                name: billingDetails.name,
                phone: billingDetails.phone,
                address: billingDetails.address
            };
        }
    
        // Confirm the card payment with Stripe
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: billingDetails
            },
            shipping: shippingDetails // This can be null or an object based on the logic above
        }).then(function(result) {
            if (result.error) {
                var errorDiv = document.getElementById('card-errors');
                var html = `
                    <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                    </span>
                    <span>${result.error.message}</span>`;
                $(errorDiv).html(html);
                $('#payment-form').fadeToggle(100);
                $('#loading-overlay').fadeToggle(100);
                card.update({ 'disabled': false});
                $('#submit-button').attr('disabled', false);
            } else {
                if (result.paymentIntent.status === 'succeeded') {
                    form.submit();
                }
            }
        });
    }).fail(function () {
        // just reload the page, the error will be in django messages
        location.reload();
    });
});