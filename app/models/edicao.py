from app.database.database import db

class Edicao(db.Model):
    __tablename__ = "edicoes"

    id = db.Column(db.Integer, primary_key=True)
    evento_id = db.Column(db.Integer, db.ForeignKey("eventos.id"), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    tema = db.Column(db.String(150), nullable=False)
    local = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    imagem_capa = db.Column(db.String(200), nullable=False)

    galerias_externas = db.relationship("GaleriaLink", backref="edicao", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Edicao {self.ano}>"