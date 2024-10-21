document.addEventListener('DOMContentLoaded', function () {
    const pickupOption = document.getElementById('pickup');
    const deliveryBillingOption = document.getElementById('delivery-billing-address');
    const btn_deliveryDifferentOption = document.getElementById('delivery-different-address');
    const billingAddressSection = document.getElementById('billing-address');
    const differentDeliveryAddress = document.getElementById('different-delivery-address');

    // Elements for updating prices
    const orderTotalElement = document.getElementById('order-total');
    const deliveryCostElement = document.getElementById('delivery-cost');
    const grandTotalElement = document.getElementById('grand-total');

    // Get delivery prices from data attributes
    const priceConfig = document.getElementById('price-config');
    const deliveryPrice = parseFloat(priceConfig.getAttribute('data-delivery-price'));
    const pickupPrice = parseFloat(priceConfig.getAttribute('data-pickup-price'));

    // Function to handle visibility of address fields
    function updateAddressFields() {
        if (pickupOption && pickupOption.checked) {
            // Hide delivery address when pick-up is chosen
            if (differentDeliveryAddress) {
                differentDeliveryAddress.classList.add('d-none');
            }
        } else if (deliveryBillingOption && deliveryBillingOption.checked) {
            // Hide delivery address when billing address = delivery address
            if (differentDeliveryAddress) {
                differentDeliveryAddress.classList.add('d-none');
            }
        } else if (btn_deliveryDifferentOption && btn_deliveryDifferentOption.checked) {
            // Show delivery address when different address delivery is chosen
            if (differentDeliveryAddress) {
                differentDeliveryAddress.classList.remove('d-none');
            }
        }
    }

    // Function to handle updating the delivery and grand total prices
    function updatePrices() {
        let deliveryCost = deliveryPrice; // Default to standard delivery cost
    
        if (pickupOption && pickupOption.checked) {
            console.log("DEBUG: Pickup option selected. Setting delivery cost to pick-up price.");
            deliveryCost = pickupPrice; // Set to pick-up price
        } else {
            console.log("DEBUG: Standard delivery option selected. Using standard delivery price.");
        }
    
        // Update the delivery cost on the page
        if (deliveryCostElement) {
            console.log(`DEBUG: Setting delivery cost to: €${deliveryCost.toFixed(2)}`);
            deliveryCostElement.textContent = `€${deliveryCost.toFixed(2)}`;
        }
    
        // Update the grand total
        if (orderTotalElement && grandTotalElement) {
            const orderTotal = parseFloat(orderTotalElement.textContent.replace('€', ''));
            const grandTotal = orderTotal + deliveryCost;
            console.log(`DEBUG: Order Total: €${orderTotal.toFixed(2)}, Delivery Cost: €${deliveryCost.toFixed(2)}, Grand Total: €${grandTotal.toFixed(2)}`);
            grandTotalElement.textContent = `€${grandTotal.toFixed(2)}`;
        }
    }
    
    // Combined function to handle all changes when a delivery option is selected
    function handleDeliveryOptionChange() {
        console.log("DEBUG: Handling change in delivery option.");
        updateAddressFields(); // Assuming this function already exists
        updatePrices();
    }
    

    // Event Listeners for order type change, with checks to ensure elements exist
    if (pickupOption) {
        pickupOption.addEventListener('change', handleDeliveryOptionChange);
    }
    if (deliveryBillingOption) {
        deliveryBillingOption.addEventListener('change', handleDeliveryOptionChange);
    }
    if (btn_deliveryDifferentOption) {
        btn_deliveryDifferentOption.addEventListener('change', handleDeliveryOptionChange);
    }

    // Set initial state on page load
    handleDeliveryOptionChange();
});

const saveAddressCheckbox = document.getElementById('id-save-address');

function toggleSaveAddressOption() {
    if (saveAddressCheckbox && saveAddressCheckbox.checked) {
        console.log("The user wants to save this address.");
    } else {
        console.log("The user does not want to save this address.");
    }
}

if (saveAddressCheckbox) {
    saveAddressCheckbox.addEventListener('change', toggleSaveAddressOption);
}
