from datetime import datetime
from sqlalchemy.orm import relationship

from app.database.database import db


class Evento(db.Model):
    __tablename__ = 'eventos'

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(140), unique=True, nullable=False, index=True)
    nome = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text)
    banner = db.Column(db.String(300))
    categoria = db.Column(db.String(80))
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    edicoes = relationship(
        'Edicao',
        back_populates='evento',
        cascade='all, delete-orphan',
        lazy=True,
        order_by='Edicao.ano.desc()'
    )

    def to_dict(self):
        return {
            'id': self.id,
            'slug': self.slug,
            'nome': self.nome,
            'descricao': self.descricao,
            'banner': self.banner,
            'categoria': self.categoria,
            'edicoes_count': len(self.edicoes)
        }

    def __repr__(self):
        return f'<Evento {self.nome} ({self.slug})>'