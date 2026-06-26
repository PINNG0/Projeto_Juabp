from datetime import datetime
from app.database.database import db

class Inscricao(db.Model):
    __tablename__ = "inscricoes"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    mensagem = db.Column(db.Text)
    ip_origem = db.Column(db.String(50))
    termo_aceite = db.Column(db.Boolean, default=True, nullable=False)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Inscricao {self.nome}>"