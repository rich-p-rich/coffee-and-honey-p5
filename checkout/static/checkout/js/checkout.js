// This code is for the pick-up & delivery options

document.addEventListener('DOMContentLoaded', function () {
    const pickupOption = document.getElementById('pickup');
    const deliveryBillingOption = document.getElementById('delivery-billing-address');
    const btn_deliveryDifferentOption = document.getElementById('delivery-different-address');
    const billingAddressSection = document.getElementById('billing-address');
    const differentDeliveryAddress = document.getElementById('different-delivery-address');

    function toggleAddressFields() {
        // Show billing address section for all options, if it exists
        if (billingAddressSection) {
            billingAddressSection.classList.remove('d-none');
        }

        if (pickupOption && pickupOption.checked) {
            // Hide delivery address for pick-up if it exists
            if (differentDeliveryAddress) {
                differentDeliveryAddress.classList.add('d-none');
            }
        } else if (deliveryBillingOption && deliveryBillingOption.checked) {
            // Hide delivery address for billing address delivery if it exists
            if (differentDeliveryAddress) {
                differentDeliveryAddress.classList.add('d-none');
            }
        } else if (btn_deliveryDifferentOption && btn_deliveryDifferentOption.checked) {
            // Show delivery address for different address delivery if it exists
            if (differentDeliveryAddress) {
                differentDeliveryAddress.classList.remove('d-none');
            }
        }
    }

    // Event Listeners for order type change, with checks to ensure elements exist
    if (pickupOption) {
        pickupOption.addEventListener('change', toggleAddressFields);
    }
    if (deliveryBillingOption) {
        deliveryBillingOption.addEventListener('change', toggleAddressFields);
    }
    if (btn_deliveryDifferentOption) {
        btn_deliveryDifferentOption.addEventListener('change', toggleAddressFields);
    }

    // Set initial state on page load
    toggleAddressFields();
});
