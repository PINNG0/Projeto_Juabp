import os
import csv
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
from models import Inscricao
from data.eventos import eventos

# =========================================
# INICIALIZAÇÃO DO APP
# =========================================
app = Flask(
    __name__,
    template_folder='../templates',
    static_folder='../static'
)

# Configurações do Banco de Dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///juabp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('SECRET_KEY', 'chave_secreta_super_segura_aqui')

# Vincula o banco de dados ao app
db.init_app(app)

# Cria as tabelas automaticamente se não existirem
with app.app_context():
    db.create_all()

# =========================================
# FUNÇÕES AUXILIARES
# =========================================
def buscar_evento_por_slug(slug):
    return next(
        (evento for evento in eventos if evento.get('slug') == slug), 
        None
    )

def obter_categorias():
    categorias = {evento.get('categoria') for evento in eventos if evento.get('categoria')}
    return sorted(categorias)

# =========================================
# ROTAS PRINCIPAIS
# =========================================
@app.route('/')
def home():
    eventos_destaque = eventos[:6]
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

    lista = eventos.copy()

    if categoria:
        lista = [e for e in lista if e.get('categoria') == categoria]

    if busca:
        busca = busca.lower().strip()
        lista = [
            e for e in lista
            if busca in e.get('nome', '').lower() or busca in e.get('descricao', '').lower()
        ]

    lista = sorted(lista, key=lambda x: x.get('nome', ''))

    return render_template(
        'eventos.html',
        eventos=lista,
        categorias=obter_categorias(),
        categoria_ativa=categoria,
        busca_ativa=busca
    )


@app.route('/evento/<slug>')
def evento_detalhe(slug):
    evento = buscar_evento_por_slug(slug)
    if not evento:
        abort(404)

    ano = request.args.get('ano')
    edicoes = evento.get('edicoes', [])

    if ano:
        edicoes = [edicao for edicao in edicoes if str(edicao.get('ano')) == ano]

    edicoes = sorted(edicoes, key=lambda x: x.get('ano', 0), reverse=True)
    anos = sorted({edicao.get('ano') for edicao in evento.get('edicoes', [])}, reverse=True)
    
    relacionados = [e for e in eventos if e.get('slug') != evento.get('slug')][:3]

    return render_template(
        'evento_detalhe.html',
        evento=evento,
        edicoes=edicoes,
        anos=anos,
        ano_ativo=ano,
        relacionados=relacionados
    )

# =========================================
# FORMULÁRIO DE INSCRIÇÃO CONECTADO AO BANCO
# =========================================
@app.route('/inscricao', methods=['GET', 'POST'])
def inscricao():
    evento_origem = request.args.get('evento', '').strip()

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        telefone = request.form.get('telefone', '').strip()
        cidade = request.form.get('cidade', '').strip()
        mensagem = request.form.get('mensagem', '').strip()

        if not nome or not telefone or not cidade:
            return render_template(
                'inscricao.html',
                erro='Preencha todos os campos obrigatórios.',
                evento_origem=evento_origem
            )

        try:
            nova_inscricao = Inscricao(
                nome=nome,
                telefone=telefone,
                cidade=cidade,
                mensagem=mensagem
            )

            db.session.add(nova_inscricao)
            db.session.commit()

            print("\n====================================")
            print("🎉 INSCRIÇÃO SALVA NO BANCO! 🎉")
            print("====================================")
            print(f"Nome:     {nome}")
            print(f"Telefone: {telefone}")
            print("====================================\n")

            flash(f'Inscrição de {nome} realizada com sucesso!')
            return render_template('inscricao.html', evento_origem=evento_origem)

        except Exception as e:
            db.session.rollback()
            print(f"ERRO DE BANCO DE DADOS: {e}")
            return render_template(
                'inscricao.html',
                erro='Ocorreu um erro ao salvar sua inscrição. Tente novamente mais tarde.',
                evento_origem=evento_origem
            )

    return render_template('inscricao.html', evento_origem=evento_origem)

# =========================================
# SISTEMA DE LOGIN & ADMINISTRAÇÃO
# =========================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        senha = request.form.get('senha')
        
        if senha == '@Tsunami2026': 
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
    return render_template('admin.html', inscritos=todas_inscricoes)

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
# TRATAMENTO DE ERROS
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