document.addEventListener('DOMContentLoaded', function() {
    const billingCheckbox = document.getElementById('billing-checkbox');
    
    // Check if billingCheckbox exists before adding the event listener
    if (billingCheckbox) {
        billingCheckbox.addEventListener('change', function() {
            if (this.checked) {
                // Set the billing address as the default delivery address
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
                        location.reload();
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
        document.getElementById('address_id').value = id;

        const form = document.getElementById('deleteAddressForm');
        form.action = `/profile/delete_address/${id}/`;

        const deleteAddressModal = new bootstrap.Modal(document.getElementById('deleteAddressModal'));
        deleteAddressModal.show();
    };
});

document.querySelectorAll('.toggle-default-btn').forEach(button => {
    button.addEventListener('click', function () {
        const addressId = this.dataset.addressId;

        fetch(`/profiles/toggle-default/${addressId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            },
        })
        .then(response => response.json())
        .then(data => {
            // Toggle the button appearance and text
            if (data.is_default) {
                this.classList.remove('btn-outline-primary');
                this.classList.add('btn-primary');
                this.textContent = "Remove Default";
                
                // Remove 'Default' designation from other buttons
                document.querySelectorAll('.toggle-default-btn').forEach(btn => {
                    if (btn !== this) {
                        btn.classList.remove('btn-primary');
                        btn.classList.add('btn-outline-primary');
                        btn.textContent = "Set as Default";
                    }
                });
            } else {
                this.classList.remove('btn-primary');
                this.classList.add('btn-outline-primary');
                this.textContent = "Set as Default";
            }
            alert(data.message);
        })
        .catch(error => console.error('Error:', error));
    });
});
