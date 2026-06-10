# models.py
from database import db

class Evento(db.Model):
    # O ID é gerado automaticamente (1, 2, 3...)
    id = db.Column(db.Integer, primary_key=True)
    
    # O Slug é a URL amigavel (ex: arraial-flor-do-maracuja-2025)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    banner = db.Column(db.String(200), nullable=False) 
    categoria = db.Column(db.String(50), nullable=False)

    # Como o Python vai mostrar esse evento no terminal se você for testar
    def __repr__(self):
        return f'<Evento {self.nome}>'