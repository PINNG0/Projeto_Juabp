import os
import csv
import secrets
import re
import json
from werkzeug.utils import secure_filename
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    abort,
    url_for,
    flash,
    session,
    Response
)

from database import db
from models import Inscricao, Usuario, Evento, Edicao, GaleriaLink

# =========================================
# INICIALIZAÇÃO DO APP
# =========================================
app = Flask(
    __name__,
    template_folder='../templates',
    static_folder='../static'
)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")

if not os.path.exists(INSTANCE_DIR):
    os.makedirs(INSTANCE_DIR)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(INSTANCE_DIR, "juabp.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('SECRET_KEY', 'chave_secreta_super_segura_aqui')

db.init_app(app)

with app.app_context():
    db.create_all()

# =========================================
# FUNÇÕES AUXILIARES E PONTE
# =========================================
def carregar_corpo_materia(descricao_str):
    """Trata a descrição antiga (texto puro) ou a nova estrutura em formato JSON safely"""
    try:
        if descricao_str and descricao_str.strip().startswith('{'):
            return json.loads(descricao_str)
    except Exception:
        pass
    return {
        'introducao': descricao_str or 'Sem descrição.',
        'imagem_corpo': '',
        'alinhamento': 'centro',
        'texto_secundario': ''
    }

def evento_para_dict(evento_obj):
    corpo = carregar_corpo_materia(evento_obj.descricao)
    return {
        'id': evento_obj.id,
        'slug': evento_obj.slug,
        'nome': evento_obj.nome,
        'banner': evento_obj.banner,
        'categoria': evento_obj.categoria,
        'introducao': corpo.get('introducao', ''),
        'imagem_corpo': corpo.get('imagem_corpo', ''),
        'alinhamento': corpo.get('alinhamento', 'centro'),
        'texto_secundario': corpo.get('texto_secundario', ''),
        'edicoes': [
            {
                'id': ed.id,
                'ano': ed.ano,
                'tema': ed.tema,
                'local': ed.local,
                'descricao': ed.descricao,
                'imagem_capa': ed.imagem_capa,
                'links': [{'nome': lnk.nome, 'url': lnk.url} for lnk in ed.galerias_externas]
            } for ed in sorted(evento_obj.edicoes, key=lambda x: x.ano, reverse=True)
        ]
    }

def obter_categorias():
    categorias = db.session.query(Evento.categoria).distinct().all()
    return sorted([cat[0] for cat in categorias if cat[0]])

# =========================================
# ROTAS PRINCIPAIS (FRONT-END)
# =========================================
@app.route('/')
def home():
    eventos_bd = Evento.query.limit(6).all()
    eventos_destaque = [evento_para_dict(e) for e in eventos_bd]
    return render_template('home.html', eventos=eventos_destaque)

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/galeria')
def galeria():
    return render_template('galeria.html')

@app.route('/eventos')
def eventos_page():
    categoria = request.args.get('categoria')
    busca = request.args.get('busca')

    query = Evento.query

    if categoria:
        query = query.filter(Evento.categoria == categoria)
    
    if busca:
        busca_formatada = f"%{busca.lower()}%"
        query = query.filter(db.or_(
            db.func.lower(Evento.nome).like(busca_formatada),
            db.func.lower(Evento.descricao).like(busca_formatada)
        ))

    eventos_bd = query.order_by(Evento.nome).all()
    lista = [evento_para_dict(e) for e in eventos_bd]

    return render_template('eventos.html', eventos=lista, categorias=obter_categorias(), categoria_ativa=categoria, busca_ativa=busca)

@app.route('/evento/<slug>')
def evento_detalhe(slug):
    evento_bd = Evento.query.filter_by(slug=slug).first_or_404()
    evento = evento_para_dict(evento_bd)

    ano = request.args.get('ano')
    edicoes = evento.get('edicoes', [])
    if ano:
        edicoes = [edicao for edicao in edicoes if str(edicao.get('ano')) == ano]

    anos = sorted({edicao.get('ano') for edicao in evento.get('edicoes', [])}, reverse=True)
    
    relacionados_bd = Evento.query.filter(Evento.slug != slug).limit(3).all()
    relacionados = [evento_para_dict(e) for e in relacionados_bd]

    return render_template('evento_detalhe.html', evento=evento, edicoes=edicoes, anos=anos, ano_ativo=ano, relacionados=relacionados)

# =========================================
# FORMULÁRIO DE INSCRIÇÃO
# =========================================
@app.route('/inscricao', methods=['GET', 'POST'])
def inscricao():
    evento_origem = request.args.get('evento', '').strip()

    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)

    if request.method == 'POST':
        token_enviado = request.form.get('csrf_token')
        if not token_enviado or token_enviado != session.get('csrf_token'):
            return render_template('inscricao.html', erro='Sessão expirada ou inválida. Por favor, tente novamente.', evento_origem=evento_origem)

        nome = request.form.get('nome', '').strip()
        telefone = request.form.get('telefone', '').strip()
        cidade = request.form.get('cidade', '').strip()
        mensagem = request.form.get('mensagem', '').strip()
        
        ip_cliente = request.headers.get('X-Forwarded-For', request.remote_addr)

        if not nome or not telefone or not cidade:
            return render_template('inscricao.html', erro='Preencha todos os campos obrigatórios.', evento_origem=evento_origem)

        try:
            nova_inscricao = Inscricao(
                nome=nome, 
                telefone=telefone, 
                cidade=cidade, 
                mensagem=mensagem,
                ip_origem=ip_cliente,
                termo_aceite=True
            )
            db.session.add(nova_inscricao)
            db.session.commit()
            flash(f'Inscrição de {nome} realizada com sucesso!')
            return render_template('inscricao.html', evento_origem=evento_origem)

        except Exception as e:
            db.session.rollback()
            print(f"ERRO DE BANCO DE DADOS: {e}")
            return render_template('inscricao.html', erro='Ocorreu um erro ao salvar sua inscrição. Tente novamente.', evento_origem=evento_origem)
        finally:
            db.session.close()

    return render_template('inscricao.html', evento_origem=evento_origem)

# =========================================
# SISTEMA ADMIN: LOGIN, LOGOUT E EXPORTAÇÃO
# =========================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)

    if request.method == 'POST':
        token_enviado = request.form.get('csrf_token')
        if not token_enviado or token_enviado != session.get('csrf_token'):
            return render_template('login.html', erro='Sessão expirada ou inválida. Por favor, tente novamente.')

        senha = request.form.get('senha')
        admin_user = Usuario.query.filter_by(username='diretoria').first()
        
        if admin_user and admin_user.check_password(senha):
            session['logado'] = True
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', erro='Senha incorreta. Acesso negado.')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logado', None)
    return redirect(url_for('home'))

@app.route('/admin')
def admin():
    if not session.get('logado'):
        return redirect(url_for('login'))
    
    todas_inscricoes = Inscricao.query.order_by(Inscricao.id.desc()).all()
    todos_eventos = Evento.query.order_by(Evento.nome).all()
    
    return render_template('admin.html', inscritos=todas_inscricoes, eventos_admin=todos_eventos)

@app.route('/admin/deletar/<int:id>', methods=['POST'])
def deletar_inscricao(id):
    if not session.get('logado'):
        return redirect(url_for('login'))
    inscricao = Inscricao.query.get_or_404(id)
    try:
        db.session.delete(inscricao)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao deletar: {e}")
    finally:
        db.session.close()
    return redirect(url_for('admin'))

@app.route('/admin/exportar')
def exportar_csv():
    if not session.get('logado'):
        return redirect(url_for('login'))
    inscricoes = Inscricao.query.order_by(Inscricao.id.desc()).all()
    def gerar_csv():
        yield 'ID,Nome,WhatsApp,Cidade,Mensagem,Data\n'
        for i in inscricoes:
            data_formatada = i.data_cadastro.strftime("%d/%m/%Y") if i.data_cadastro else ""
            msg = i.mensagem.replace('\n', ' ').replace('\r', '') if i.mensagem else '---'
            yield f'{i.id},{i.nome},{i.telefone},{i.cidade},{msg},{data_formatada}\n'
    return Response(gerar_csv(), mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=inscricoes_juabp.csv'})

# =========================================
# SISTEMA ADMIN: CMS DE EVENTOS STRUCT
# =========================================
@app.route('/admin/evento/novo', methods=['GET', 'POST'])
def admin_evento_novo():
    if not session.get('logado'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        nome = request.form.get('nome').strip()
        categoria = request.form.get('categoria').strip()
        
        # Elementos da matéria estruturada
        introducao = request.form.get('introducao').strip()
        alinhamento = request.form.get('alinhamento').strip()
        texto_secundario = request.form.get('texto_secundario').strip()
        
        # Uploads de imagem
        banner_file = request.files.get('banner_file')
        banner_url = request.form.get('banner_url').strip()
        corpo_file = request.files.get('corpo_file')
        corpo_url = request.form.get('corpo_url').strip()

        slug_base = re.sub(r'[^a-zA-Z0-9]', '-', nome.lower())
        slug = re.sub(r'-+', '-', slug_base).strip('-')

        if not nome or not categoria:
            flash("Erro: Nome e Categoria são obrigatórios.", "error")
            return render_template('admin_evento_form.html')

        # Processa Banner de Capa
        nome_banner = 'campea.jpeg'
        if banner_file and banner_file.filename:
            filename = secure_filename(banner_file.filename)
            banner_file.save(os.path.join(app.static_folder, 'img', filename))
            nome_banner = filename
        elif banner_url:
            nome_banner = banner_url

        # Processa Imagem de Notícia do Corpo
        nome_imagem_corpo = ''
        if corpo_file and corpo_file.filename:
            filename = secure_filename(corpo_file.filename)
            corpo_file.save(os.path.join(app.static_folder, 'img', filename))
            nome_imagem_corpo = filename
        elif corpo_url:
            nome_imagem_corpo = corpo_url

        # Empacota a estrutura da notícia em formato JSON textual
        noticia_json = json.dumps({
            'introducao': introducao,
            'imagem_corpo': nome_imagem_corpo,
            'alinhamento': alinhamento,
            'texto_secundario': texto_secundario
        }, ensure_ascii=False)

        try:
            novo_evento = Evento(
                slug=slug,
                nome=nome,
                descricao=noticia_json,
                banner=nome_banner,
                categoria=categoria
            )
            db.session.add(novo_evento)
            db.session.commit()
            
            flash(f"Sucesso: O evento '{nome}' foi criado com sucesso!", "success")
            return redirect(url_for('admin'))
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao salvar: {e}")
            flash("Erro crítico ao tentar salvar o evento.", "error")

    return render_template('admin_evento_form.html')

@app.route('/admin/evento/editar/<int:id>', methods=['GET', 'POST'])
def admin_evento_editar(id):
    if not session.get('logado'):
        return redirect(url_for('login'))

    evento = Evento.query.get_or_404(id)
    corpo_atual = carregar_corpo_materia(evento.descricao)

    if request.method == 'POST':
        evento.nome = request.form.get('nome').strip()
        evento.categoria = request.form.get('categoria').strip()
        
        introducao = request.form.get('introducao').strip()
        alinhamento = request.form.get('alinhamento').strip()
        texto_secundario = request.form.get('texto_secundario').strip()

        # Upload Banner
        banner_file = request.files.get('banner_file')
        banner_url = request.form.get('banner_url').strip()
        if banner_file and banner_file.filename:
            filename = secure_filename(banner_file.filename)
            banner_file.save(os.path.join(app.static_folder, 'img', filename))
            evento.banner = filename
        elif banner_url:
            evento.banner = banner_url

        # Upload Imagem Corpo
        corpo_file = request.files.get('corpo_file')
        corpo_url = request.form.get('corpo_url').strip()
        nome_imagem_corpo = corpo_atual.get('imagem_corpo', '')
        
        if corpo_file and corpo_file.filename:
            filename = secure_filename(corpo_file.filename)
            corpo_file.save(os.path.join(app.static_folder, 'img', filename))
            nome_imagem_corpo = filename
        elif corpo_url:
            nome_imagem_corpo = corpo_url

        # Monta o novo JSON atualizado
        evento.descricao = json.dumps({
            'introducao': introducao,
            'imagem_corpo': nome_imagem_corpo,
            'alinhamento': alinhamento,
            'texto_secundario': texto_secundario
        }, ensure_ascii=False)

    try:
        db.session.commit()
        flash(f"Sucesso: O evento '{evento.nome}' foi atualizado!", "success")
        return redirect(url_for('admin'))
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao atualizar: {e}")
        flash("Erro crítico ao atualizar o evento.", "error")

    evento_mapeado = evento_para_dict(evento)
    return render_template('admin_evento_editar.html', evento=evento_mapeado)

@app.route('/admin/evento/deletar/<int:id>', methods=['POST'])
def admin_evento_deletar(id):
    if not session.get('logado'):
        return redirect(url_for('login'))
    evento = Evento.query.get_or_404(id)
    nome_evento = evento.nome
    try:
        db.session.delete(evento)
        db.session.commit()
        flash(f"Sucesso: O evento '{nome_evento}' foi excluído definitivamente.", "success")
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao deletar: {e}")
        flash("Erro ao tentar excluir o evento.", "error")
    return redirect(url_for('admin'))

# =========================================
# SISTEMA ADMIN: CMS DE EDIÇÕES E GALERIAS
# =========================================
@app.route('/admin/evento/<int:evento_id>/edicoes')
def admin_edicoes(evento_id):
    if not session.get('logado'):
        return redirect(url_for('login'))
    evento = Evento.query.get_or_404(evento_id)
    edicoes = Edicao.query.filter_by(evento_id=evento.id).order_by(Edicao.ano.desc()).all()
    return render_template('admin_edicoes.html', evento=evento, edicoes=edicoes)

@app.route('/admin/evento/<int:evento_id>/edicao/nova', methods=['GET', 'POST'])
def admin_edicao_nova(evento_id):
    if not session.get('logado'):
        return redirect(url_for('login'))
    evento = Evento.query.get_or_404(evento_id)

    if request.method == 'POST':
        ano = request.form.get('ano', type=int)
        tema = request.form.get('tema').strip()
        local = request.form.get('local').strip()
        descricao = request.form.get('descricao').strip()

        capa_file = request.files.get('capa_file')
        capa_url = request.form.get('capa_url').strip()
        
        nome_capa = 'campea.jpeg'
        if capa_file and capa_file.filename:
            filename = secure_filename(capa_file.filename)
            capa_file.save(os.path.join(app.static_folder, 'img', filename))
            nome_capa = filename
        elif capa_url:
            nome_capa = capa_url

        try:
            nova_edicao = Edicao(
                evento_id=evento.id,
                ano=ano,
                tema=tema,
                local=local,
                descricao=descricao,
                imagem_capa=nome_capa
            )
            db.session.add(nova_edicao)
            db.session.flush()

            link_nomes = request.form.getlist('link_nome[]')
            link_urls = request.form.getlist('link_url[]')
            
            for nome_link, url_link in zip(link_nomes, link_urls):
                if nome_link.strip() and url_link.strip():
                    novo_link = GaleriaLink(edicao_id=nova_edicao.id, nome=nome_link.strip(), url=url_link.strip())
                    db.session.add(novo_link)

            db.session.commit()
            flash(f"Sucesso: A edição de {ano} foi adicionada ao evento!", "success")
            return redirect(url_for('admin_edicoes', evento_id=evento.id))
            
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao salvar edição: {e}")
            flash("Erro ao salvar a edição. Verifique os dados.", "error")

    return render_template('admin_edicao_form.html', evento=evento)

@app.route('/admin/edicao/deletar/<int:id>', methods=['POST'])
def admin_edicao_deletar(id):
    if not session.get('logado'):
        return redirect(url_for('login'))
    edicao = Edicao.query.get_or_404(id)
    evento_id = edicao.evento_id
    try:
        GaleriaLink.query.filter_by(edicao_id=edicao.id).delete()
        db.session.delete(edicao)
        db.session.commit()
        flash(f"Edição excluída com sucesso.", "success")
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao deletar edição: {e}")
        flash("Erro ao excluir a edição.", "error")
    return redirect(url_for('admin_edicoes', evento_id=evento_id))

# =========================================
# ERROS
# =========================================
@app.errorhandler(404)
def pagina_nao_encontrada(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def erro_interno(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    print("\n====================================")
    print("🔥 SERVIDOR INICIANDO...")
    print("🌐 http://127.0.0.1:5000")
    print("====================================\n")
    app.run(debug=True, host='0.0.0.0', port=5000)