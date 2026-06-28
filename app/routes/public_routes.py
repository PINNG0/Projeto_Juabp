import os
import secrets
from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    session,
    redirect,
    url_for,
    current_app
)
from werkzeug.utils import secure_filename

from app.database.database import db
from app.models.usuario import Usuario
from app.services.evento_service import EventoService
from app.services.inscricao_service import InscricaoService
from app.services.instagram_service import InstagramService
from app.services.usuario_service import UsuarioService
from app.repositories.usuario_repository import UsuarioRepository

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def home():
    posts = InstagramService.get_recent_posts()
    eventos = EventoService.obter_home_eventos()
    return render_template('home.html', eventos=eventos, posts=posts)

@public_bp.route('/sobre')
def sobre():
    return render_template('sobre.html')

@public_bp.route('/galeria')
def galeria():
    return render_template('galeria.html')

@public_bp.route('/eventos')
def eventos_page():
    categoria = request.args.get('categoria')
    busca = request.args.get('busca')
    return render_template(
        'eventos.html',
        eventos=EventoService.listar_eventos(categoria, busca),
        categorias=EventoService.obter_categorias(),
        categoria_ativa=categoria,
        busca_ativa=busca
    )

@public_bp.route('/evento/<slug>')
def evento_detalhe(slug):
    ano = request.args.get('ano')
    evento, edicoes, anos, relacionados = EventoService.obter_detalhe_evento(slug, ano)
    return render_template(
        'evento_detalhe.html',
        evento=evento, edicoes=edicoes, anos=anos, ano_ativo=ano, relacionados=relacionados
    )

@public_bp.route('/inscricao', methods=['GET', 'POST'])
def inscricao():
    ev_origem = request.args.get('evento', '').strip()

    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)

    if request.method == 'POST':
        token = request.form.get('csrf_token')

        if token != session.get('csrf_token'):
            return render_template('inscricao.html', erro='Sessão expirada.', evento_origem=ev_origem)

        nome = request.form.get('nome', '').strip()
        telefone = request.form.get('telefone', '').strip()
        cidade = request.form.get('cidade', '').strip()
        mensagem = request.form.get('mensagem', '').strip()

        if not nome or not telefone or not cidade:
            return render_template('inscricao.html', erro='Preencha os campos obrigatórios.', evento_origem=ev_origem)

        try:
            InscricaoService.criar_inscricao(
                nome, telefone, cidade, mensagem, request.headers.get('X-Forwarded-For', request.remote_addr)
            )
            flash(f'Inscrição de {nome} realizada com sucesso!', 'sucesso')
            return redirect(url_for('public.inscricao'))
        except Exception:
            return render_template('inscricao.html', erro='Erro ao salvar a inscrição.', evento_origem=ev_origem)

    return render_template('inscricao.html', evento_origem=ev_origem)


# ==========================================
# ROTA: PERFIL DO USUÁRIO LOGADO
# ==========================================
@public_bp.route('/perfil', methods=['GET', 'POST'])
def perfil():
    if not session.get('usuario_id'):
        flash('Faça login para acessar o seu perfil.', 'erro')
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        try:
            # Mandamos o trabalho pesado para o Service!
            usuario = UsuarioService.atualizar_perfil(
                session['usuario_id'], 
                request.form, 
                request.files.get('foto_perfil')
            )
            session['nome_completo'] = usuario.nome_completo
            flash('Perfil atualizado com sucesso!', 'sucesso')
        except Exception as e:
            flash(f'Erro ao salvar: {str(e)}', 'erro')
            
        return redirect(url_for('public.perfil'))
        
    # GET: Apenas busca e exibe a página
    usuario = UsuarioRepository.buscar_por_id(session['usuario_id'])
    return render_template('perfil.html', usuario=usuario)