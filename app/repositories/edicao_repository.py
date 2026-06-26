from app.database.database import db
from app.models import Edicao

class EdicaoRepository:
    @staticmethod
    def obter_por_evento(evento_id):
        return Edicao.query.filter_by(evento_id=evento_id).order_by(Edicao.ano.desc()).all()

    @staticmethod
    def sa_objeto_id(id):
        return Edicao.query.get_or_404(id)

    @staticmethod
    def salvar(edicao):
        db.session.add(edicao)
        db.session.commit()

    @staticmethod
    def adicionar_relacionado(objeto):
        db.session.add(objeto)
        db.session.commit()

    @staticmethod
    def deletar(edicao):
        db.session.delete(edicao)
        db.session.commit()