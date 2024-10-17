document.addEventListener('DOMContentLoaded', function () {
    const pickupOption = document.getElementById('pickup');
    const deliveryOption = document.getElementById('delivery');
    const deliveryAddress = document.getElementById('delivery-address');
    const saveDeliveryInfo = document.getElementById('save-delivery-info');

    // Hide the delivery address and save option if "Pick-Up" is selected
    if (pickupOption) {
        pickupOption.addEventListener('change', function () {
            if (this.checked) {
                deliveryAddress.classList.add('d-none');
                saveDeliveryInfo.classList.add('d-none');
            }
        });
    }

    // Show the delivery address and save option if "Delivery" is selected
    if (deliveryOption) {
        deliveryOption.addEventListener('change', function () {
            if (this.checked) {
                deliveryAddress.classList.remove('d-none');
                saveDeliveryInfo.classList.remove('d-none');
            }
        });
    }

    // Initially hide or show based on the default checked radio
    if (pickupOption && pickupOption.checked) {
        deliveryAddress.classList.add('d-none');
        saveDeliveryInfo.classList.add('d-none');
    }
});
