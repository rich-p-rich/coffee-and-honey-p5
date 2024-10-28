document.addEventListener('DOMContentLoaded', function() {
    const billingCheckbox = document.getElementById('billing-checkbox');
    
    // Check if billingCheckbox exists before adding the event listener
    if (billingCheckbox) {
        billingCheckbox.addEventListener('change', function() {
            if (this.checked) {
                // Send request to set the billing address as the default delivery address
                fetch("{% url 'set_billing_as_default' %}", {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': '{{ csrf_token }}',
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ default_delivery: true })
                })
                .then(response => {
                    if (response.ok) {
                        alert("Billing address is now the default delivery address.");
                        location.reload(); // Refresh to update UI
                    } else {
                        alert("Failed to set default delivery address.");
                    }
                })
                .catch(error => console.error('Error:', error));
            }
        });
    }

    // Function to set the address ID for the delete modal
    window.setAddressId = function(id) {
        // Set the hidden input field
        document.getElementById('address_id').value = id;

        // Dynamically set the form action URL
        const form = document.getElementById('deleteAddressForm');
        form.action = `/profile/delete_address/${id}/`;

        // Manually show the modal
        const deleteAddressModal = new bootstrap.Modal(document.getElementById('deleteAddressModal'));
        deleteAddressModal.show();
    };
});
