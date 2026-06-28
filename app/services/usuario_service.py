from datetime import datetime
from app.repositories.usuario_repository import UsuarioRepository
from app.services.upload_service import UploadService
from app.database.database import db

class UsuarioService:
    @staticmethod
    def atualizar_perfil(usuario_id, form_dados, foto_file):
        usuario = UsuarioRepository.buscar_por_id(usuario_id)
        
        if not usuario:
            raise ValueError("Usuário não encontrado.")

        # Atualiza textos básicos
        usuario.nome_completo = form_dados.get('nome_completo', '').strip()
        usuario.telefone = form_dados.get('telefone', '').strip()
        usuario.cidade = form_dados.get('cidade', '').strip()
        usuario.estado = form_dados.get('estado', '').strip()
        usuario.biografia = form_dados.get('biografia', '').strip()
        usuario.instagram_link = form_dados.get('instagram_link', '').strip()

        # Tratamento da Data
        data_nasc_str = form_dados.get('data_nascimento')
        if data_nasc_str:
            try:
                usuario.data_nascimento = datetime.strptime(data_nasc_str, '%Y-%m-%d').date()
            except ValueError:
                pass 

        # Reaproveitando o SEU UploadService (Adeus gambiarra de os.makedirs!)
        if foto_file and foto_file.filename != '':
            nome_foto = UploadService.salvar_imagem(foto_file)
            usuario.foto_perfil = nome_foto

        db.session.commit()
        return usuario