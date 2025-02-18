document.addEventListener('DOMContentLoaded', function() {
    const menuHamburguesa = document.querySelector('.menu-hamburguesa');
    const menuNavegacion = document.querySelector('.menu-navegacion');
    
    menuHamburguesa.addEventListener('click', function() {
        menuHamburguesa.classList.toggle('activo');
        menuNavegacion.classList.toggle('activo');
    });

    document.querySelectorAll('.enlace-nav, .boton-nav').forEach(enlace => {
        enlace.addEventListener('click', () => {
            menuHamburguesa.classList.remove('activo');
            menuNavegacion.classList.remove('activo');
        });
    });

    window.addEventListener('scroll', () => {
        if(menuNavegacion.classList.contains('activo')) {
            menuHamburguesa.classList.remove('activo');
            menuNavegacion.classList.remove('activo');
        }
    });
});