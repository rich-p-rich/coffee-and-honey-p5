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

    // 1. Function to check if the delivery address differs from the billing address
    function deliveryAddressDiffersFromBilling() {
        if (!defaultDeliveryData) return false;

        const billingName = document.getElementById('id_billing_full_name').value;
        const billingStreet = document.getElementById('id_billing_street_address1').value;
        const billingPostcode = document.getElementById('id_billing_postcode').value;

        return (
            defaultDeliveryData.delivery_name !== billingName ||
            defaultDeliveryData.delivery_street_address1 !== billingStreet ||
            defaultDeliveryData.delivery_postcode !== billingPostcode
        );
    }

    // 2. Function to set the default delivery option based on address data
    function setDefaultDeliveryOption() {
        if (deliveryAddressDiffersFromBilling()) {
            deliveryDifferentRadio.checked = true;
            populateWithDefaultDeliveryData();
            differentDeliveryAddress.classList.remove('d-none');
        } else {
            deliveryBillingRadio.checked = true;
            differentDeliveryAddress.classList.add('d-none');
        }
    }

    // Populate delivery fields with default delivery data if it exists
    function populateWithDefaultDeliveryData() {
        if (defaultDeliveryData) {
            document.getElementById('id_delivery_name').value = defaultDeliveryData.delivery_name || '';
            document.getElementById('id_delivery_street_address1').value = defaultDeliveryData.delivery_street_address1 || '';
            document.getElementById('id_delivery_street_address2').value = defaultDeliveryData.delivery_street_address2 || '';
            document.getElementById('id_delivery_town_or_city').value = defaultDeliveryData.delivery_town_or_city || '';
            document.getElementById('id_delivery_county').value = defaultDeliveryData.delivery_county || '';
            document.getElementById('id_delivery_postcode').value = defaultDeliveryData.delivery_postcode || '';
            document.getElementById('id_delivery_country').value = defaultDeliveryData.delivery_country || '';
        }
    }

    // Enable customer to select saved addresses (visible only if authenticated)
    const savedAddressDropdown = document.getElementById('saved-address-dropdown');
    const savedAddressSelect = document.getElementById('saved_address');
    if (savedAddressSelect) {
        savedAddressSelect.addEventListener('change', populateAddressFields);
    }

    // Populate delivery address fields based on saved address selection
    function populateAddressFields() {
        const selectedOption = savedAddressSelect.options[savedAddressSelect.selectedIndex];
        if (!selectedOption.value) return;

        document.getElementById('id_delivery_name').value = selectedOption.getAttribute('data-recipient-name') || '';
        document.getElementById('id_delivery_street_address1').value = selectedOption.getAttribute('data-street-address1') || '';
        document.getElementById('id_delivery_street_address2').value = selectedOption.getAttribute('data-street-address2') || '';
        document.getElementById('id_delivery_town_or_city').value = selectedOption.getAttribute('data-town-or-city') || '';
        document.getElementById('id_delivery_county').value = selectedOption.getAttribute('data-county') || '';
        document.getElementById('id_delivery_postcode').value = selectedOption.getAttribute('data-postcode') || '';
        document.getElementById('id_delivery_country').value = selectedOption.getAttribute('data-country') || '';
    }

    // Get delivery prices from data attributes
    const priceConfig = document.getElementById('price-config');
    const deliveryPrice = parseFloat(priceConfig.getAttribute('data-delivery-price'));
    const pickupPrice = parseFloat(priceConfig.getAttribute('data-pickup-price'));

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

    // Function to update address visibility based on selected delivery option
    function updateAddressFields() {
        if (pickupRadio && pickupRadio.checked) {
            differentDeliveryAddress.classList.add('d-none');
            if (savedAddressDropdown) savedAddressDropdown.style.display = 'none';
        } else if (deliveryBillingRadio && deliveryBillingRadio.checked) {
            differentDeliveryAddress.classList.add('d-none');
            if (savedAddressDropdown) savedAddressDropdown.style.display = 'none';
        } else if (deliveryDifferentRadio && deliveryDifferentRadio.checked) {
            differentDeliveryAddress.classList.remove('d-none');
            if (savedAddressDropdown) savedAddressDropdown.style.display = 'block';
        }
    }

    // Initial setup on page load
    setDefaultDeliveryOption();
    handleDeliveryOptionChange();

    // Event listeners for delivery option changes
    pickupRadio.addEventListener('change', handleDeliveryOptionChange);
    deliveryBillingRadio.addEventListener('change', handleDeliveryOptionChange);
    deliveryDifferentRadio.addEventListener('change', handleDeliveryOptionChange);
});