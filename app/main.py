import os
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    abort,
    url_for,
    flash
)

from data.eventos import eventos

# =========================================
# INICIALIZAÇÃO DO APP
# =========================================
app = Flask(
    __name__,
    template_folder='../templates',
    static_folder='../static'
)

# Melhor Prática: Busca a chave secreta no ambiente (segurança) ou usa uma padrão para testes
app.secret_key = os.environ.get('SECRET_KEY', 'chave_secreta_super_segura_aqui')

# =========================================
# FUNÇÕES AUXILIARES
# =========================================
def buscar_evento_por_slug(slug):
    """Retorna o evento correspondente ao slug ou None se não encontrar."""
    return next(
        (evento for evento in eventos if evento.get('slug') == slug), 
        None
    )

def obter_categorias():
    """Gera uma lista ordenada sem repetições das categorias de eventos."""
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
    
    # Pega até 3 eventos relacionados excluindo o atual
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
# FORMULÁRIO DE INSCRIÇÃO
# =========================================
@app.route('/inscricao', methods=['GET', 'POST'])
def inscricao():
    if request.method == 'POST':
        # O .strip() limpa espaços em branco acidentais digitados pelo usuário
        nome = request.form.get('nome', '').strip()
        telefone = request.form.get('telefone', '').strip()
        cidade = request.form.get('cidade', '').strip()
        mensagem = request.form.get('mensagem', '').strip()

        if not nome or not telefone or not cidade:
            return render_template(
                'inscricao.html',
                erro='Preencha todos os campos obrigatórios.'
            )

        print("\n====================================")
        print("🎉 NOVA INSCRIÇÃO RECEBIDA 🎉")
        print("====================================")
        print(f"Nome:     {nome}")
        print(f"Telefone: {telefone}")
        print(f"Cidade:   {cidade}")
        if mensagem:
            print(f"Mensagem: {mensagem}")
        print("====================================\n")

        flash(f'Inscrição de {nome} realizada com sucesso!')
        return render_template('inscricao.html')

    return render_template('inscricao.html')

# =========================================
# TRATAMENTO DE ERROS
# =========================================
@app.errorhandler(404)
def pagina_nao_encontrada(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def erro_interno(error):
    return render_template('500.html'), 500

# =========================================
# INICIAR SERVIDOR
# =========================================
if __name__ == '__main__':
    print("\n====================================")
    print("🔥 SERVIDOR INICIANDO...")
    print("🌐 http://127.0.0.1:5000")
    print("====================================\n")
    app.run(debug=True, host='0.0.0.0', port=5000)