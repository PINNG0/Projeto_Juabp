# app/models/inscricao.py
from datetime import datetime
from app.database.database import db

class Inscricao(db.Model):
    __tablename__ = 'inscricoes'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    telefone = db.Column(db.String(50), nullable=False)
    cidade = db.Column(db.String(120), nullable=True)
    mensagem = db.Column(db.Text, nullable=True)
    ip_origem = db.Column(db.String(100), nullable=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'telefone': self.telefone,
            'cidade': self.cidade,
            'mensagem': self.mensagem,
            'ip_origem': self.ip_origem,
            'data_cadastro': self.data_cadastro.isoformat() if self.data_cadastro else None
        }

    def to_csv_row(self):
        """Retorna uma tupla/string pronta para export CSV (sanitizada)."""
        data = self.data_cadastro.strftime('%d/%m/%Y') if self.data_cadastro else ''
        msg = (self.mensagem or '').replace('\n', ' ').replace('\r', '')
        return (self.id, self.nome, self.telefone, self.cidade or '', msg or '---', data)

    def __repr__(self):
        return f"<Inscricao {self.nome} - {self.telefone}>"
