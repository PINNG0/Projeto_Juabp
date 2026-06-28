from app.repositories.usuario_repository import UsuarioRepository

class AuthService:
    @staticmethod
    def validar_login(username, senha):
        usuario = UsuarioRepository.buscar_por_username(username)
        # Retorna o objeto do usuário inteiro se a senha bater, ou None se falhar
        if usuario and usuario.check_password(senha):
            return usuario
        return None