// Update quantity on click
$('.update-link').click(function(e) {
    e.preventDefault();
    var form = $(this).prev('.update-form');
    console.log("Submitting form with the following data:");
    form.find("input").each(function() {
        console.log($(this).attr('name') + ": " + $(this).val());
    });
    form.submit();
});

// Remove item and reload on click
$('.remove-item').click(function(e) {
    e.preventDefault();
    
    // Get CSRF token from a hidden input field or cookie
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    var itemId = $(this).attr('id').split('remove_')[1];
    var size = $(this).data('product_size');
    var url = `/bag/remove/${itemId}/`;
    var data = {
        'csrfmiddlewaretoken': csrfToken,
        'product_size': size
    };

    $.post(url, data)
        .done(function() {
            location.reload();
        });
});

function openModal() {
    var myModal = new bootstrap.Modal(document.getElementById('signInModal'));
    myModal.show();
}
