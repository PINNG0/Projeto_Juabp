import secrets
from flask import Blueprint, render_template, request, redirect, url_for, session
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'csrf_token' not in session: 
        session['csrf_token'] = secrets.token_hex(16)
        
    if request.method == 'POST':
        token = request.form.get('csrf_token')
        if not token or token != session.get('csrf_token'):
            return render_template('login.html', erro='Sessão inválida.')
            
        senha = request.form.get('senha')
        
        # A Rota agora pergunta para o Service, e não para o Banco de Dados!
        if AuthService.validar_login('diretoria', senha):
            session['logado'] = True
            return redirect(url_for('admin.admin'))
            
        return render_template('login.html', erro='Senha incorreta.')
        
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('logado', None)
    return redirect(url_for('public.home'))