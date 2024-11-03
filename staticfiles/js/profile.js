document.addEventListener('DOMContentLoaded', function() {
    const billingCheckbox = document.getElementById('billing-checkbox');

    // CSRF token retrieval function
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Retrieve CSRF token and store it in `csrftoken`
    const csrftoken = getCookie('csrftoken');

    // Check if billingCheckbox exists before adding the event listener
    if (billingCheckbox) {
        billingCheckbox.addEventListener('change', function() {
            if (this.checked) {
                // Send request to set the billing address as the default delivery address
                fetch("{% url 'set_billing_as_default' %}", {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken,
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

    // Add event listeners for "Set as Default" or "Remove Default" buttons
    document.querySelectorAll('.toggle-default-btn').forEach(button => {
        button.addEventListener('click', function() {
            const addressId = this.dataset.addressId;
            const isDefault = this.innerText.includes("Remove Default");

            if (isDefault) {
                // Remove default designation and revert to billing address
                fetch('/profile/set_billing_as_default/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ default_delivery: true })
                })
                .then(response => {
                    if (response.ok) {
                        alert("Default designation removed. Billing address is now the presumed default.");
                        location.reload(); // Refresh to update UI
                    } else {
                        alert("Failed to remove default designation.");
                    }
                })
                .catch(error => console.error('Error:', error));
            } else {
                // Set the clicked address as the default delivery address
                fetch(`/profile/set_default_address/${addressId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken,
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => {
                    if (response.ok) {
                        alert("Default address has been updated.");
                        location.reload(); // Refresh to update UI
                    } else {
                        alert("Failed to set default address.");
                    }
                })
                .catch(error => console.error('Error:', error));
            }
        });
    });
});
