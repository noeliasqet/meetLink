function toggleMenu() {
    document.getElementById('navbar').classList.toggle('show');
}

document.addEventListener('click', function(e) {
    const navbar = document.getElementById('navbar');
    const toggleButton = document.querySelector('button[onclick="toggleMenu()"]');
    if (!navbar.contains(e.target) && !toggleButton.contains(e.target)) {
        navbar.classList.remove('show');
    }
});
