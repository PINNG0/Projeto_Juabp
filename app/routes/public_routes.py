import secrets
from flask import Blueprint, render_template, request, flash, session
from app.services.evento_service import EventoService
from app.services.inscricao_service import InscricaoService
from app.services.instagram_service import InstagramService

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
    cat = request.args.get('categoria')
    busca = request.args.get('busca')
    return render_template('eventos.html', 
                           eventos=EventoService.listar_eventos(cat, busca), 
                           categorias=EventoService.obter_categorias(), 
                           categoria_ativa=cat, 
                           busca_ativa=busca)

@public_bp.route('/evento/<slug>')
def evento_detalhe(slug):
    ano = request.args.get('ano')
    evento, edicoes, anos, relacionados = EventoService.obter_detalhe_evento(slug, ano)
    return render_template('evento_detalhe.html', evento=evento, edicoes=edicoes, anos=anos, ano_ativo=ano, relacionados=relacionados)

@public_bp.route('/inscricao', methods=['GET', 'POST'])
def inscricao():
    ev_origem = request.args.get('evento', '').strip()
    if 'csrf_token' not in session: session['csrf_token'] = secrets.token_hex(16)
        
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        tel = request.form.get('telefone', '').strip()
        cid = request.form.get('cidade', '').strip()
        
        if not nome or not tel or not cid: 
            return render_template('inscricao.html', erro='Preencha os campos obrigatórios.', evento_origem=ev_origem)
            
        try:
            InscricaoService.criar_inscricao(
                nome, tel, cid, 
                request.form.get('mensagem', '').strip(), 
                request.headers.get('X-Forwarded-For', request.remote_addr)
            )
            flash(f'Inscricao de {nome} realizada com sucesso!')
        except Exception:
            return render_template('inscricao.html', erro='Erro ao salvar a inscrição. Tente novamente.', evento_origem=ev_origem)
            
    return render_template('inscricao.html', evento_origem=ev_origem)