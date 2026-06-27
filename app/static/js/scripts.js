// Máscara automática para o campo de telefone (WhatsApp)
document.addEventListener('DOMContentLoaded', function() {
    const telefoneInput = document.getElementById('telefone');
    
    if (telefoneInput) {
        telefoneInput.addEventListener('input', function (e) {
            let x = e.target.value.replace(/\D/g, '').match(/(\d{0,2})(\d{0,5})(\d{0,4})/);
            e.target.value = !x[2] ? x[1] : '(' + x[1] + ') ' + x[2] + (x[3] ? '-' + x[3] : '');
        });
    }
});

// ==========================================
// CONTROLE DO DROPDOWN MENU
// ==========================================
document.addEventListener("DOMContentLoaded", function() {
    const btnUserMenu = document.getElementById("btnUserMenu");
    const userMenu = document.getElementById("userMenu");

    // Verifica se o botão existe na página antes de adicionar o evento
    if (btnUserMenu && userMenu) {
        
        // Abre e fecha ao clicar no botão
        btnUserMenu.addEventListener("click", function(event) {
            // Previne que o clique se propague e feche imediatamente
            event.stopPropagation(); 
            userMenu.classList.toggle("show");
        });

        // Fecha o menu se clicar em qualquer outro lugar da tela
        window.addEventListener("click", function(event) {
            if (!event.target.closest('.user-dropdown')) {
                if (userMenu.classList.contains("show")) {
                    userMenu.classList.remove("show");
                }
            }
        });
    }
});