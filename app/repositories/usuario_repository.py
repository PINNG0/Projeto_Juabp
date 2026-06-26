from app.models import Usuario

class UsuarioRepository:
    @staticmethod
    def buscar_por_username(username):
        return Usuario.query.filter_by(username=username).first()