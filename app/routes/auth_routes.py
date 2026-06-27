from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from app.models.usuario import Usuario

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not password:
            flash('Preencha usuário e senha.', 'erro')
            return render_template('login.html')

        usuario = Usuario.query.filter_by(username=username).first()

        if usuario and usuario.check_password(password):
            session.clear()

            session['usuario_id'] = usuario.id
            session['username'] = usuario.username
            session['cargo'] = usuario.cargo
            session.permanent = True

            if usuario.is_admin():
                return redirect(url_for('admin.admin'))

            return redirect(url_for('public.home'))

        flash('Usuário ou senha incorretos.', 'erro')

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))