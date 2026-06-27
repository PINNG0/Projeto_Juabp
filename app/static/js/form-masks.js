document.addEventListener('DOMContentLoaded', () => {
    const telefone = document.getElementById('telefone');

    if (!telefone) return;

    telefone.addEventListener('input', (e) => {
        let v = e.target.value.replace(/\D/g, '');

        v = v.replace(/(\d{2})(\d)/, '($1) $2');
        v = v.replace(/(\d{5})(\d)/, '$1-$2');

        e.target.value = v;
    });
});