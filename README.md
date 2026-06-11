# 🌟 JUABP - O Tsunami do Norte | Site Oficial

> **"Mais do que uma quadrilha, um movimento de força, identidade e tradição na cultura de Rondônia."**

Este é o repositório oficial do site da **Juventude Unida pelo Amor da Bom Pastor (JUABP)**, uma das agremiações folclóricas juninas mais tradicionais, antigas e vitoriosas de Porto Velho, Rondônia. O projeto foi desenvolvido para modernizar a presença digital da quadrilha, exibindo sua rica história (tetracampeã do Flor do Maracujá), catálogo de eventos e um sistema inteligente de captação de novos integrantes.

---

## 🚀 Funcionalidades Principais

* **📖 Biografia Imersiva:** Linha do tempo interativa e histórico das conquistas e enredos marcantes (como o marco de 2006, *O Auto da Compadecida* e *Lampião*).
* **🎭 Catálogo de Eventos:** Exibição dinâmica de eventos com sistema de filtros por ano e categorias (Festivais, Ensaios, etc.).
* **📝 Sistema de Inscrição Inteligente:** Formulário conectado a um banco de dados real. Capta inscrições gerais e possui "URL Tracking" (preenche automaticamente a origem caso o usuário clique em inscrever-se a partir de um evento específico).
* **🔒 Painel da Diretoria (Admin):** Área administrativa para visualização das inscrições recebidas, com integração direta para o WhatsApp dos inscritos.
* **📱 Design Responsivo:** Interface moderna, com tema escuro (Dark Mode nativo), uso de gradientes e totalmente adaptada para dispositivos móveis.

---

## 🛠️ Tecnologias e Arquitetura

O projeto foi construído utilizando um backend em Python leve e eficiente, focado em renderização rápida e gestão simplificada de banco de dados.

* **Backend:** Python 3, Flask
* **Banco de Dados:** SQLite, Flask-SQLAlchemy (ORM)
* **Frontend:** HTML5, CSS3 Customizado (Variáveis, Flexbox, CSS Grid), Jinja2 (Templating)
* **Arquitetura:** Application Factory Pattern adaptada e separação de Models, Database e Rotas.

---

## 📂 Estrutura do Projeto

```text
juabp-site/
├── app/
│   ├── main.py              # Arquivo principal (Rotas e inicialização)
│   ├── database.py          # Configuração Singleton do SQLAlchemy
│   ├── models.py            # Modelos de dados (Inscricao, Evento)
│   └── data/
│       └── eventos.py       # Banco de dados estático/dicionário do catálogo
├── instance/
│   └── juabp.db             # Banco de dados SQLite (Auto-gerado)
├── static/
│   ├── css/                 # Arquivos de estilo modulares (base, layout, pages...)
│   ├── img/                 # Assets de imagem, banners e logos
│   └── js/                  # Scripts de interação e animação
├── templates/
│   ├── base.html            # Layout mestre (Header, Footer, Meta tags)
│   ├── home.html            # Página inicial
│   ├── sobre.html           # História e linha do tempo
│   ├── eventos.html         # Lista de eventos e filtros
│   ├── evento_detalhe.html  # Página de espetáculo específico
│   ├── inscricao.html       # Formulário de novos brincantes
│   ├── admin.html           # Dashboard da diretoria
│   └── 404.html             # Tratamento de página não encontrada
└── README.md

⚙️ Como Executar o Projeto Localmente
Siga os passos abaixo para rodar o site em sua máquina:

1. Clone o repositório
    git clone [https://github.com/PINNG0/Projeto_Juabp](https://github.com/PINNG0/Projeto_Juabp)
    cd juabp-site

2. Crie e ative um Ambiente Virtual (Recomendado)
No Windows:
    python -m venv venv
    venv\Scripts\activate

No Linux/Mac:
    python3 -m venv venv
    source venv/bin/activate

3. Instale as dependências:
    pip install Flask Flask-SQLAlchemy

4. Execute o servidor
    cd app
    python main.py
O terminal exibirá a confirmação de que o servidor está rodando. O banco de dados juabp.db será gerado automaticamente na primeira execução.
Acesse no seu navegador: http://127.0.0.1:5000

🛣️ Roadmap / Próximos Passos
[ ] Autenticação de Segurança (Login/Senha) para a rota /admin.

[ ] Criação de Página de Galeria Fotográfica de alto impacto.

[ ] Deploy em servidor de produção (Render / Heroku / PythonAnywhere).

📜 Licença e Direitos Autorais
© 2026 Junina Juventude Unida pelo Amor da Bom Pastor (JUABP). Todos os direitos reservados. Projeto de uso exclusivo da agremiação.