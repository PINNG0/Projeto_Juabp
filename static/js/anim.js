// anim.js

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        // Quando o elemento entra na tela...
        if (entry.isIntersecting) {
            entry.target.classList.add('show');
            
            // Opcional: Se quiser que a animação aconteça só uma vez (não repita ao subir a tela)
            // observer.unobserve(entry.target); 
        }
    });
}, {
    threshold: 0.2 // Dispara quando 20% do elemento aparece na tela
});

// Seleciona os elementos da nossa nova arquitetura
const elementosParaAnimar = document.querySelectorAll('.timeline-item, .diretor, .event-box, .stat-card, .box');

elementosParaAnimar.forEach(el => {
    // Esconde eles inicialmente (via CSS) e manda o JS observar
    observer.observe(el);
});