from app.database.database import db

class Evento(db.Model):
    __tablename__ = "eventos"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    banner = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)

    edicoes = db.relationship("Edicao", backref="evento", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Evento {self.nome}>"