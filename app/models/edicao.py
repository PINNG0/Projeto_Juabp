# app/models/edicao.py

from datetime import datetime
from sqlalchemy.orm import relationship
from app.database.database import db

class Edicao(db.Model):
    __tablename__ = 'edicoes'

    id = db.Column(db.Integer, primary_key=True)
    evento_id = db.Column(db.Integer, db.ForeignKey('eventos.id', ondelete='CASCADE'), nullable=False, index=True)
    ano = db.Column(db.Integer, nullable=False, index=True)
    tema = db.Column(db.String(200), nullable=True)
    local = db.Column(db.String(200), nullable=True)
    descricao = db.Column(db.Text, nullable=True)
    imagem_capa = db.Column(db.String(300), nullable=True)  # nome do arquivo ou URL
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    # Relações
    evento = relationship('Evento', back_populates='edicoes')
    galerias_externas = relationship('GaleriaLink', back_populates='edicao', cascade='all, delete-orphan', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'evento_id': self.evento_id,
            'ano': self.ano,
            'tema': self.tema,
            'local': self.local,
            'descricao': self.descricao,
            'imagem_capa': self.imagem_capa,
            'criado_em': self.criado_em.isoformat() if self.criado_em else None,
            'galerias_externas': [g.to_dict() for g in self.galerias_externas] if self.galerias_externas is not None else []
        }

    def __repr__(self):
        return f"<Edicao {self.ano} - {self.tema}>"
