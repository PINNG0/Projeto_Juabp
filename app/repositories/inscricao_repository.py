from app.database.database import db
from app.models import Inscricao

class InscricaoRepository:
    @staticmethod
    def obter_todas():
        return Inscricao.query.order_by(Inscricao.id.desc()).all()

    @staticmethod
    def buscar_por_id(id):
        return Inscricao.query.get_or_404(id)

    @staticmethod
    def salvar(inscricao):
        db.session.add(inscricao)
        db.session.commit()

    @staticmethod
    def deletar(inscricao):
        db.session.delete(inscricao)
        db.session.commit()