# app/models/evento.py
from datetime import datetime
from sqlalchemy.orm import relationship
from app.database.database import db

class Evento(db.Model):
    __tablename__ = 'eventos'

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(140), unique=True, nullable=False, index=True)
    nome = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=True)  # pode conter JSON empacotado pelo mapper
    banner = db.Column(db.String(300), nullable=True)  # pode ser URL externa ou nome de arquivo
    categoria = db.Column(db.String(80), nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    # Relação com edições (one-to-many)
    edicoes = relationship('Edicao', back_populates='evento', cascade='all, delete-orphan', lazy='dynamic')

    def to_dict(self):
        """Representação simplificada para templates/serialização."""
        return {
            'id': self.id,
            'slug': self.slug,
            'nome': self.nome,
            'descricao': self.descricao,
            'banner': self.banner,
            'categoria': self.categoria,
            'edicoes_count': self.edicoes.count() if self.edicoes is not None else 0
        }

    def __repr__(self):
        return f"<Evento {self.nome} ({self.slug})>"
