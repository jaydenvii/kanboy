function toggleNavBurger() {
    const navbar_burger = document.getElementById('navbar-burger');
    const navbar_menu = document.getElementById('navbar-menu');

    navbar_burger.classList.toggle('is-active');
    navbar_menu.classList.toggle('is-active');
}