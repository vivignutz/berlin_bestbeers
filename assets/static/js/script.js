// Remove flash message alert after 3 seconds
document.addEventListener('DOMContentLoaded', removeAlerts);

function removeAlerts() {
    setTimeout(function () {
        let messages = document.getElementById('msg');
        let alert = new bootstrap.Alert(messages);
        alert.close();
    }, 3000);
}


$('.star-rating .fa-star').on('click', function () {
    var rating = $(this).data('rating');
    $('#rating').val(rating);
    $(this).siblings().removeClass('checked');
    $(this).addClass('checked');
});