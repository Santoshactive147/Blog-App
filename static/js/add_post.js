
// Example of basic form validation and error handling using JavaScript
document.getElementById('blog-form').addEventListener('submit', function (event) {
    var formValid = true;

    // Check if title is empty
    if (document.getElementById('title').value.trim() === "") {
        formValid = false;
    }

    // Check if content is empty
    if (document.getElementById('content').value.trim() === "") {
        formValid = false;
    }

    // If form is invalid, prevent submission and show error message
    if (!formValid) {
        event.preventDefault();
        document.getElementById('error-message').style.display = 'block';
    }
});
