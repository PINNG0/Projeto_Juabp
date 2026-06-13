from database import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# =========================================
# SEGURANÇA: SISTEMA DE USUÁRIOS (ADMIN)
# =========================================
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    # Função que pega a senha digitada e transforma em um código indecifrável (Hash)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Função que checa se a senha digitada no login bate com o Hash salvo
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Usuario {self.username}>'


# =========================================
# SISTEMA DE EVENTOS (CMS RELACIONAL)
# =========================================
class Evento(db.Model):
    __tablename__ = 'eventos'
    
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    banner = db.Column(db.String(200), nullable=False) 
    categoria = db.Column(db.String(50), nullable=False)
    
    # Relação 1 para N: Um evento pode ter várias edições (anos)
    edicoes = db.relationship('Edicao', backref='evento', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Evento {self.nome}>'


class Edicao(db.Model):
    __tablename__ = 'edicoes'
    
    id = db.Column(db.Integer, primary_key=True)
    evento_id = db.Column(db.Integer, db.ForeignKey('eventos.id'), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    tema = db.Column(db.String(150), nullable=False)
    local = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    imagem_capa = db.Column(db.String(200), nullable=False)
    
    # Relação 1 para N: Uma edição pode ter vários links (Fotto, Drive, etc.)
    galerias_externas = db.relationship('GaleriaLink', backref='edicao', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Edicao {self.ano} - {self.tema}>'


class GaleriaLink(db.Model):
    __tablename__ = 'galeria_links'
    
    id = db.Column(db.Integer, primary_key=True)
    edicao_id = db.Column(db.Integer, db.ForeignKey('edicoes.id'), nullable=False)
    nome = db.Column(db.String(50), nullable=False) # Ex: "Ver na Fotto", "Ver no Drive"
    url = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        return f'<Link {self.nome}>'


# =========================================
# REGISTROS E LGPD
# =========================================
class Inscricao(db.Model):
    __tablename__ = 'inscricoes'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    mensagem = db.Column(db.Text, nullable=True) 
    
    # LGPD: Auditoria e Proteção Legal
    ip_origem = db.Column(db.String(50), nullable=True)
    termo_aceite = db.Column(db.Boolean, default=True, nullable=False)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Inscricao {self.nome}>'