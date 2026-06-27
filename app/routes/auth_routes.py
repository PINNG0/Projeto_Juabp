from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.usuario import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Rota de Autenticação Universal."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        # Procura o usuário
        usuario = Usuario.query.filter_by(username=username).first()
        
        # Valida as credenciais
        if usuario and usuario.check_password(password):
            # Cria a sessão profissional
            session['usuario_id'] = usuario.id
            session['username'] = usuario.username
            session['cargo'] = usuario.cargo
            
            # Sem mensagens de 'Bem-vindo'. Roteamento inteligente:
            if usuario.is_admin():
                # Se for admin (diretoria), vai para admin_routes.admin()
                return redirect(url_for('admin.admin'))
            else:
                # Se for outro cargo, vai para a home pública
                return redirect(url_for('public.home'))
            
        # Única mensagem de erro necessária.
        flash('Usuário ou senha incorretos.', 'erro')
        
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    """Finaliza a sessão."""
    session.clear()
    return redirect(url_for('auth.login'))