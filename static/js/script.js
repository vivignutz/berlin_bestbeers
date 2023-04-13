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



const ratingStars = document.querySelector('.rating-stars');
const rating = ratingStars.querySelectorAll('.rating');
const ratingInput = document.querySelector('#id_rating');

stars.forEach((star, index) => {
    star.addEventListener('click', () => {
        ratingInput.value = index + 1;
        ratingStars.setAttribute('data-rating', index + 1);
    });
});