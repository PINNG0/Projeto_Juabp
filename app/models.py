from database import db
from datetime import datetime

class Evento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    banner = db.Column(db.String(200), nullable=False) 
    categoria = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Evento {self.nome}>'

class Inscricao(db.Model):
    __tablename__ = 'inscricoes'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    mensagem = db.Column(db.Text, nullable=True) 
    
    # Registra automaticamente a data e hora que a pessoa enviou o formulário
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Inscricao {self.nome}>'