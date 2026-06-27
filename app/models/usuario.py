from app.database.database import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    
    # COLUNAS: HIERARQUIA E STATUS
    nome_completo = db.Column(db.String(100), nullable=True)
    cargo = db.Column(db.String(20), default='visitante') # 'visitante', 'brincante', 'coreografo', 'diretoria'
    status = db.Column(db.String(20), default='ativo') # 'ativo', 'inativo'
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    # NOVAS COLUNAS: PERFIL (Para Rede Social e Contato)
    biografia = db.Column(db.String(255), nullable=True)
    telefone = db.Column(db.String(20), nullable=True)
    foto_perfil = db.Column(db.String(255), default='default_perfil.png')
    instagram_link = db.Column(db.String(150), nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.cargo == 'diretoria'

    def __repr__(self):
        return f"<Usuario {self.username}>"

# ==========================================
# NOVA TABELA: MURAL DA JUABP (Intranet)
# ==========================================
class AvisoInterno(db.Model):
    __tablename__ = 'avisos_internos'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    tipo = db.Column(db.String(20), default='geral') # 'geral', 'ensaio', 'musica', 'figurino'
    link_anexo = db.Column(db.String(255), nullable=True) 
    data_postagem = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relação com o Usuário (quem postou o aviso)
    autor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    autor = db.relationship('Usuario', backref=db.backref('avisos', lazy=True))