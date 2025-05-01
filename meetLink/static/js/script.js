function toggleMenu() {
    const navbar = document.getElementById('navbar');
    const toggleButton = document.getElementById('toggle-button');
    navbar.classList.toggle('show');
    toggleButton.classList.toggle('open');
}

function handleResize() {
    const navbar = document.getElementById('navbar');
    const toggleButton = document.getElementById('toggle-button');

    if (window.innerWidth >= 768) {
        navbar.classList.add('show');
    } else if (!toggleButton.classList.contains('open')) {
        navbar.classList.remove('show');
    }
}

window.addEventListener('resize', handleResize);
window.addEventListener('DOMContentLoaded', handleResize);

document.addEventListener('click', function(e) {
    const navbar = document.getElementById('navbar');
    const toggleButton = document.getElementById('toggle-button');

    // Cierra el navbar también si se hace clic fuera
    if (!navbar.contains(e.target) && !toggleButton.contains(e.target)) {
        navbar.classList.remove('show');
        toggleButton.classList.remove('open');
    }
});
