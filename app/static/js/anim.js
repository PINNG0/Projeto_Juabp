const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('show');
        }
    });
}, {
    threshold: 0.2
});

const elementos = document.querySelectorAll(
    '.timeline-item, .diretor, .event-box, .stat-card, .box'
);

elementos.forEach(el => observer.observe(el));