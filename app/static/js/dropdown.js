document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("btnUserMenu");
    const menu = document.getElementById("userMenu");

    if (!btn || !menu) return;

    btn.addEventListener("click", (e) => {
        e.stopPropagation();
        menu.classList.toggle("show");
    });

    document.addEventListener("click", () => {
        menu.classList.remove("show");
    });
});