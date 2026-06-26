
from app.database.database import db
from app.models import Evento

class EventoRepository:
    @staticmethod
    def obter_limite(limite):
        return Evento.query.limit(limite).all()

    @staticmethod
    def buscar_todos():
        return Evento.query.order_by(Evento.nome).all()

    @staticmethod
    def buscar_por_id(id):
        return Evento.query.get_or_404(id)

    @staticmethod
    def buscar_por_slug(slug):
        return Evento.query.filter_by(slug=slug).first_or_404()

    @staticmethod
    def buscar_relacionados(slug_atual, limite):
        return Evento.query.filter(Evento.slug != slug_atual).limit(limite).all()

    @staticmethod
    def obter_categorias():
        categorias = db.session.query(Evento.categoria).distinct().all()
        return sorted([cat[0] for cat in categorias if cat[0]])

    @staticmethod
    def filtrar_eventos(categoria=None, busca=None):
        query = Evento.query
        if categoria:
            query = query.filter(Evento.categoria == categoria)
        if busca:
            busca_formatada = f"%{busca.lower()}%"
            query = query.filter(db.or_(
                db.func.lower(Evento.nome).like(busca_formatada),
                db.func.lower(Evento.descricao).like(busca_formatada)
            ))
        return query.order_by(Evento.nome).all()

    @staticmethod
    def salvar(evento):
        db.session.add(evento)
        db.session.commit()

    @staticmethod
    def sa_alteracao_direta():
        db.session.commit()

    @staticmethod
    def deletar(evento):
        db.session.delete(evento)
        db.session.commit()