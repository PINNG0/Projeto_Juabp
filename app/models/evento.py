from datetime import datetime
from sqlalchemy.orm import relationship
from app.database.database import db

class Evento(db.Model):
    __tablename__ = 'eventos'

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(140), unique=True, nullable=False, index=True)
    nome = db.Column(db.String(200), nullable=False)
    banner = db.Column(db.String(300))
    categoria = db.Column(db.String(80))
    
    # ==========================================
    # NOVAS COLUNAS REAIS (Fim do empacotamento)
    # ==========================================
    introducao = db.Column(db.Text, nullable=True)
    imagem_corpo = db.Column(db.String(300), nullable=True)
    alinhamento = db.Column(db.String(20), default='centro')
    texto_secundario = db.Column(db.Text, nullable=True)

    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    edicoes = relationship(
        'Edicao',
        back_populates='evento',
        cascade='all, delete-orphan',
        lazy=True,
        order_by='Edicao.ano.desc()'
    )

    def to_dict(self):
        # Mapeamos 'introducao' como 'descricao' também, para não quebrar os HTMLs antigos (home.html)
        return {
            'id': self.id,
            'slug': self.slug,
            'nome': self.nome,
            'descricao': self.introducao or '',
            'banner': self.banner,
            'categoria': self.categoria,
            'introducao': self.introducao or '',
            'imagem_corpo': self.imagem_corpo or '',
            'alinhamento': self.alinhamento or 'centro',
            'texto_secundario': self.texto_secundario or '',
            'edicoes_count': len(self.edicoes),
            'edicoes': [ed.to_dict() for ed in self.edicoes]
        }

    def __repr__(self):
        return f'<Evento {self.nome} ({self.slug})>'