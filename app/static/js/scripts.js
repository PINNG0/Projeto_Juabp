// ==========================================
// 1. MÁSCARA AUTOMÁTICA (TELEFONE/WHATSAPP)
// ==========================================
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
// 2. CONTROLE DO DROPDOWN MENU DO UTILIZADOR
// ==========================================
document.addEventListener("DOMContentLoaded", function() {
    const btnUserMenu = document.getElementById("btnUserMenu");
    const userMenu = document.getElementById("userMenu");

    if (btnUserMenu && userMenu) {
        btnUserMenu.addEventListener("click", function(event) {
            event.stopPropagation(); 
            userMenu.classList.toggle("show");
        });

        window.addEventListener("click", function(event) {
            if (!event.target.closest('.user-dropdown')) {
                if (userMenu.classList.contains("show")) {
                    userMenu.classList.remove("show");
                }
            }
        });
    }
});

// ==========================================
// 3. COMPORTAMENTO DA PÁGINA DE PERFIL (UPLOAD FOTO)
// ==========================================
document.addEventListener("DOMContentLoaded", function() {
    const fotoPerfilInput = document.getElementById('foto_perfil');
    
    if (fotoPerfilInput) {
        fotoPerfilInput.addEventListener('change', function(e) {
            if(e.target.files.length > 0) {
                let label = document.getElementById('label_foto');
                if (label) {
                    label.innerHTML = "✅ Imagem Selecionada";
                    label.style.borderColor = "var(--accent)";
                    label.style.color = "var(--accent)";
                }
            }
        });
    }
});