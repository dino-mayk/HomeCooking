function togglePassword(){
    var input = document.getElementById('password');
    var icon = document.getElementById('icon');
    if (input.type === "password") {
        input.type = "text";
        icon.className = "bi bi-eye";
    }
    else {
        input.type = "password";
        icon.className = "bi bi-eye-slash";
    }
}