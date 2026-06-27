# app/models/galeria_link.py
from datetime import datetime
from app.database.database import db

class GaleriaLink(db.Model):
    __tablename__ = 'galeria_links'

    id = db.Column(db.Integer, primary_key=True)
    edicao_id = db.Column(db.Integer, db.ForeignKey('edicoes.id', ondelete='CASCADE'), nullable=False, index=True)
    nome = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(1000), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    # Relação inversa
    edicao = db.relationship('Edicao', back_populates='galerias_externas')

    def to_dict(self):
        return {
            'id': self.id,
            'edicao_id': self.edicao_id,
            'nome': self.nome,
            'url': self.url,
            'criado_em': self.criado_em.isoformat() if self.criado_em else None
        }

    def __repr__(self):
        return f"<GaleriaLink {self.nome}>"
