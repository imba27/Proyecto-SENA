document.addEventListener('DOMContentLoaded', () => {
    const menuHamburguesa = document.querySelector('.menu-hamburguesa');
    const menuNavegacion = document.querySelector('.menu-navegacion');

    menuHamburguesa.addEventListener('click', () => {
        menuHamburguesa.classList.toggle('activo');
        menuNavegacion.classList.toggle('activo');
    });

    // Cerrar menú al hacer clic en un enlace
    document.querySelectorAll('.enlace-nav').forEach(enlace => {
        enlace.addEventListener('click', () => {
            menuHamburguesa.classList.remove('activo');
            menuNavegacion.classList.remove('activo');
        });
    });
});
