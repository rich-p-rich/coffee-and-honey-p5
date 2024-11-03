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

    const csrftoken = getCookie('csrftoken');
    const messageContainer = document.getElementById('message-container');

    // Check if billingCheckbox exists before adding the event listener
    if (billingCheckbox) {
        billingCheckbox.addEventListener('change', function() {
            if (this.checked) {
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
                        displayMessage("Billing address is now the default delivery address.");
                        location.reload(); // Refresh to update UI
                    } else {
                        displayMessage("Failed to set default delivery address.", "alert-danger");
                    }
                })
                .catch(error => console.error('Error:', error));
            }
        });
    }

    function displayMessage(message, type="alert-success") {
        messageContainer.style.display = "block";
        messageContainer.className = `alert ${type}`;
        messageContainer.textContent = message;
    }

    document.querySelectorAll('.toggle-default-btn').forEach(button => {
        button.addEventListener('click', function() {
            const addressId = this.dataset.addressId;
            const isDefault = this.innerText.includes("Remove Default");

            if (isDefault) {
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
                        displayMessage("Default designation removed. Billing address is now the presumed default.");
                        location.reload(); // Refresh to update UI
                    } else {
                        displayMessage("Failed to remove default designation.", "alert-danger");
                    }
                })
                .catch(error => console.error('Error:', error));
            } else {
                fetch(`/profile/set_default_address/${addressId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken,
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => {
                    if (response.ok) {
                        displayMessage("Default address has been updated.");
                        location.reload(); // Refresh to update UI
                    } else {
                        displayMessage("Failed to set default address.", "alert-danger");
                    }
                })
                .catch(error => console.error('Error:', error));
            }
        });
    });
});
