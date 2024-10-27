document.addEventListener('DOMContentLoaded', function () {

    // Elements for updating prices
    const orderTotalElement = document.querySelector('.order-total');
    const deliveryCostElement = document.querySelector('.delivery-cost');
    const grandTotalElement = document.querySelector('.grand-total');

    // Delivery and Pickup options    
    const pickupRadio = document.getElementById('pickup');
    const deliveryBillingRadio = document.getElementById('delivery-billing-same');
    const deliveryDifferentRadio = document.getElementById('delivery-different');
    const differentDeliveryAddress = document.getElementById('delivery-address-section');

    // For using saved addresses in profile to populate a different delivery address
    const savedAddressDropdown = document.getElementById('saved-address-dropdown');
    const savedAddressSelect = document.getElementById('saved_address');

    // Get delivery prices from data attributes
    const priceConfig = document.getElementById('price-config');
    const deliveryPrice = parseFloat(priceConfig.getAttribute('data-delivery-price'));
    const pickupPrice = parseFloat(priceConfig.getAttribute('data-pickup-price'));

    function updateAddressFields() {
        if (pickupRadio && pickupRadio.checked) {
            // Hide delivery address when pick-up is chosen
            if (differentDeliveryAddress) {
                differentDeliveryAddress.classList.add('d-none');
            }
            if (savedAddressDropdown) {
                savedAddressDropdown.style.display = 'none';
            }
        } else if (deliveryBillingRadio && deliveryBillingRadio.checked) {
            // Hide delivery address when billing address = delivery address
            if (differentDeliveryAddress) {
                differentDeliveryAddress.classList.add('d-none');
            }
            if (savedAddressDropdown) {
                savedAddressDropdown.style.display = 'none';
            }
        } else if (deliveryDifferentRadio && deliveryDifferentRadio.checked) {
            // Show delivery address and saved address dropdown when different address delivery is chosen
            if (differentDeliveryAddress) {
                differentDeliveryAddress.classList.remove('d-none');
            }
            if (savedAddressDropdown) {
                savedAddressDropdown.style.display = 'block';
            }
        }
    }
    
    // Populate delivery address fields based on saved_address selection
    function populateAddressFields() {
        const selectedOption = savedAddressSelect.options[savedAddressSelect.selectedIndex];
        if (!selectedOption.value) return;
    
        // Fetch data attributes from the selected option
        const recipientName = selectedOption.getAttribute('data-recipient-name');
        const streetAddress1 = selectedOption.getAttribute('data-street-address1');
        const streetAddress2 = selectedOption.getAttribute('data-street-address2');
        const townOrCity = selectedOption.getAttribute('data-town-or-city');
        const county = selectedOption.getAttribute('data-county');
        const postcode = selectedOption.getAttribute('data-postcode');
        const country = selectedOption.getAttribute('data-country');
    
        // Set delivery address fields with the fetched data
        document.getElementById('id_delivery_name').value = recipientName;
        document.getElementById('id_delivery_street_address1').value = streetAddress1;
        document.getElementById('id_delivery_street_address2').value = streetAddress2 || '';
        document.getElementById('id_delivery_town_or_city').value = townOrCity;
        document.getElementById('id_delivery_county').value = county || '';
        document.getElementById('id_delivery_postcode').value = postcode;
        document.getElementById('id_delivery_country').value = country;
    }
    
    // Event Listener for the saved address dropdown
    savedAddressSelect.addEventListener('change', populateAddressFields);

    // Function to ensure delivery fields are visible before submitting the form
    function ensureDeliveryFieldsVisible() {
        if (deliveryDifferentRadio && deliveryDifferentRadio.checked) {
            // Ensure fields are shown before form submission
            differentDeliveryAddress.classList.remove('d-none');
        }
    }

    // Function to handle updating the delivery and grand total prices
    function updatePrices() {
        let deliveryCost = deliveryPrice; // Default to standard delivery cost
    
        if (pickupRadio && pickupRadio.checked) {
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
        updateAddressFields(); // Ensure fields are toggled correctly
        updatePrices();
    }

    // Event Listeners for order type change, with checks to ensure elements exist
    if (pickupRadio) {
        pickupRadio.addEventListener('change', handleDeliveryOptionChange);
    }
    if (deliveryBillingRadio) {
        deliveryBillingRadio.addEventListener('change', handleDeliveryOptionChange);
    }
    if (deliveryDifferentRadio) {
        deliveryDifferentRadio.addEventListener('change', handleDeliveryOptionChange);
    }

    // Set initial state on page load
    handleDeliveryOptionChange();

    // Add ensure function to form submission
    const checkoutForm = document.querySelector('form');
    if (checkoutForm) {
        checkoutForm.addEventListener('submit', ensureDeliveryFieldsVisible);
    }

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
});