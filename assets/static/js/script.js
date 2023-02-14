// Remove flash message alert after 3 seconds
document.addEventListener('DOMContentLoaded', removeAlerts);

function removeAlerts() {
    setTimeout(function () {
        let messages = document.getElementById('msg');
        let alert = new bootstrap.Alert(messages);
        alert.close();
    }, 3000);
}