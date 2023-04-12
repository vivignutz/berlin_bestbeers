// Remove flash message alert after 3 seconds
document.addEventListener('DOMContentLoaded', removeAlerts);

function removeAlerts() {
    setTimeout(function () {
        let messages = document.getElementById('msg');
        let alert = new bootstrap.Alert(messages);
        alert.close();
    }, 3000);
}


$(document).ready(function () {
    // Updates the stars CSS class based on the user's current rating

    $('.star-rating .fa-star').click(function () {
        var rating = $(this).data('rating');
        $('.star-rating .fa-star').removeClass('checked');
        $('.star-rating .fa-star').each(function () {
            if ($(this).data('rating') <= rating) {
                $(this).addClass('checked');
            }
        });
        $('#rating-value').val(rating);
    });
});

$(document).ready(function () {
    // Sends the user's rating to the server when they click the "Rate it!" button
    $('.rating-form').submit(function (event) {
        event.preventDefault();
        var form = $(this);
        var rating = $('#rating-value').val();
        var itemId = $('.star-rating').data('item-id');
        $.ajax({
            type: 'POST',
            url: form.attr('action'),
            data: {
                'rating': rating,
                'item_id': itemId,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function (data) {
                alert('Evaluation successfully sent!');
            },
            error: function () {
                alert('Oh, weee... An error occurred while sending the evaluation. Please try again later..');
            }
        });
    });
});