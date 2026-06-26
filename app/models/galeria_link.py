from app.database.database import db

class GaleriaLink(db.Model):
    __tablename__ = "galeria_links"

    id = db.Column(db.Integer, primary_key=True)
    edicao_id = db.Column(db.Integer, db.ForeignKey("edicoes.id"), nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        return f"<Link {self.nome}>"