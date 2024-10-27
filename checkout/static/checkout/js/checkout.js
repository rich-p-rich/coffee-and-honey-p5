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

    // Default delivery data if different from billing address
    const defaultDeliveryElement = document.getElementById('default_delivery_data');
    let defaultDeliveryData = null;

    // Check if default delivery element exists before parsing
    if (defaultDeliveryElement) {
        defaultDeliveryData = JSON.parse(defaultDeliveryElement.textContent);
    }

    // Enable customer to select saved addresses
    const savedAddressDropdown = document.getElementById('saved-address-dropdown');
    const savedAddressSelect = document.getElementById('saved_address');

    // Get delivery prices from data attributes
    const priceConfig = document.getElementById('price-config');
    const deliveryPrice = parseFloat(priceConfig.getAttribute('data-delivery-price'));
    const pickupPrice = parseFloat(priceConfig.getAttribute('data-pickup-price'));

    // Function to update address visibility based on selected delivery option
    function updateAddressFields() {
        if (pickupRadio && pickupRadio.checked) {
            differentDeliveryAddress.classList.add('d-none');
            savedAddressDropdown.style.display = 'none';
        } else if (deliveryBillingRadio && deliveryBillingRadio.checked) {
            differentDeliveryAddress.classList.add('d-none');
            savedAddressDropdown.style.display = 'none';
        } else if (deliveryDifferentRadio && deliveryDifferentRadio.checked) {
            differentDeliveryAddress.classList.remove('d-none');
            savedAddressDropdown.style.display = 'block';
        }
    }

    // Populate delivery fields with default delivery data if it exists
    function populateWithDefaultDeliveryData() {
        if (defaultDeliveryData) {
            deliveryDifferentRadio.checked = true; // Select "Deliver to Different Address"
            differentDeliveryAddress.classList.remove('d-none'); // Show the delivery address section

            // Populate fields with default delivery data
            document.getElementById('id_delivery_name').value = defaultDeliveryData.delivery_name || '';
            document.getElementById('id_delivery_street_address1').value = defaultDeliveryData.delivery_street_address1 || '';
            document.getElementById('id_delivery_street_address2').value = defaultDeliveryData.delivery_street_address2 || '';
            document.getElementById('id_delivery_town_or_city').value = defaultDeliveryData.delivery_town_or_city || '';
            document.getElementById('id_delivery_county').value = defaultDeliveryData.delivery_county || '';
            document.getElementById('id_delivery_postcode').value = defaultDeliveryData.delivery_postcode || '';
            document.getElementById('id_delivery_country').value = defaultDeliveryData.delivery_country || '';
        }
    }

    // Populate fields on page load if default delivery data is present
    if (defaultDeliveryData) {
        populateWithDefaultDeliveryData();
        updateAddressFields();
    }

    // Populate delivery address fields based on saved address selection
    function populateAddressFields() {
        const selectedOption = savedAddressSelect.options[savedAddressSelect.selectedIndex];
        if (!selectedOption.value) return;
        
        // Fetch data attributes from selected option
        document.getElementById('id_delivery_name').value = selectedOption.getAttribute('data-recipient-name') || '';
        document.getElementById('id_delivery_street_address1').value = selectedOption.getAttribute('data-street-address1') || '';
        document.getElementById('id_delivery_street_address2').value = selectedOption.getAttribute('data-street-address2') || '';
        document.getElementById('id_delivery_town_or_city').value = selectedOption.getAttribute('data-town-or-city') || '';
        document.getElementById('id_delivery_county').value = selectedOption.getAttribute('data-county') || '';
        document.getElementById('id_delivery_postcode').value = selectedOption.getAttribute('data-postcode') || '';
        document.getElementById('id_delivery_country').value = selectedOption.getAttribute('data-country') || '';
    }

    // Event listener for the saved address dropdown
    savedAddressSelect.addEventListener('change', populateAddressFields);

    // Ensure delivery fields are visible before form submission
    function ensureDeliveryFieldsVisible() {
        if (deliveryDifferentRadio.checked) {
            differentDeliveryAddress.classList.remove('d-none');
        }
    }

    // Function to update delivery and grand total prices
    function updatePrices() {
        let deliveryCost = deliveryPrice;

        if (pickupRadio && pickupRadio.checked) {
            deliveryCost = pickupPrice;
        }

        // Update the displayed delivery cost and grand total
        if (deliveryCostElement) deliveryCostElement.textContent = `€${deliveryCost.toFixed(2)}`;
        if (orderTotalElement && grandTotalElement) {
            const orderTotal = parseFloat(orderTotalElement.textContent.replace('€', ''));
            grandTotalElement.textContent = `€${(orderTotal + deliveryCost).toFixed(2)}`;
        }
    }

    // Handle changes in delivery options
    function handleDeliveryOptionChange() {
        updateAddressFields();
        updatePrices();
    }

    // Event listeners for delivery option changes
    if (pickupRadio) pickupRadio.addEventListener('change', handleDeliveryOptionChange);
    if (deliveryBillingRadio) deliveryBillingRadio.addEventListener('change', handleDeliveryOptionChange);
    if (deliveryDifferentRadio) deliveryDifferentRadio.addEventListener('change', handleDeliveryOptionChange);

    // Initial setup on page load
    handleDeliveryOptionChange();

    // Ensure delivery fields are visible before form submission
    const checkoutForm = document.querySelector('form');
    if (checkoutForm) checkoutForm.addEventListener('submit', ensureDeliveryFieldsVisible);

    // Toggle save address option in the console (for debugging purposes)
    const saveAddressCheckbox = document.getElementById('id-save-address');
    function toggleSaveAddressOption() {
        console.log(saveAddressCheckbox && saveAddressCheckbox.checked ? "The user wants to save this address." : "The user does not want to save this address.");
    }
    if (saveAddressCheckbox) saveAddressCheckbox.addEventListener('change', toggleSaveAddressOption);
});
