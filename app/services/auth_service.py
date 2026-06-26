from app.repositories.usuario_repository import UsuarioRepository

class AuthService:
    @staticmethod
    def validar_login(username, senha):
        usuario = UsuarioRepository.buscar_por_username(username)
        if usuario and usuario.check_password(senha):
            return True
        return False