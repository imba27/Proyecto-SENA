document.addEventListener('DOMContentLoaded', function() {
    const menuHamburguesa = document.querySelector('.menu-hamburguesa');
    const menuNavegacion = document.querySelector('.menu-navegacion');
    const usuarioDropdown = document.querySelector('.usuario-dropdown');
    
    // Hamburger menu toggle
    menuHamburguesa.addEventListener('click', function() {
        menuHamburguesa.classList.toggle('activo');
        menuNavegacion.classList.toggle('activo');
    });

    // Close navigation menu when nav links are clicked
    document.querySelectorAll('.enlace-nav, .boton-nav').forEach(enlace => {
        enlace.addEventListener('click', () => {
            menuHamburguesa.classList.remove('activo');
            menuNavegacion.classList.remove('activo');
        });
    });

    // Close navigation menu on scroll
    window.addEventListener('scroll', () => {
        if(menuNavegacion.classList.contains('activo')) {
            menuHamburguesa.classList.remove('activo');
            menuNavegacion.classList.remove('activo');
        }
    });

    // User dropdown functionality
    if (usuarioDropdown) {
        const usuarioIcono = usuarioDropdown.querySelector('.icono-login');
        
        // Toggle dropdown on click
        usuarioIcono.addEventListener('click', function(e) {
            e.preventDefault();
            usuarioDropdown.classList.toggle('activo');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (usuarioDropdown && !usuarioDropdown.contains(e.target)) {
                usuarioDropdown.classList.remove('activo');
            }
        });

        // Prevent dropdown close when clicking inside dropdown
        usuarioDropdown.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    }
});