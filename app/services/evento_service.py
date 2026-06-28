import re
from app.repositories.evento_repository import EventoRepository
from app.services.upload_service import UploadService
from app.models import Evento

class EventoService:
    @staticmethod
    def obter_home_eventos():
        eventos = EventoRepository.obter_limite(6)
        return [e.to_dict() for e in eventos]

    @staticmethod
    def obter_categorias():
        return EventoRepository.obter_categorias()

    @staticmethod
    def listar_eventos(categoria=None, busca=None):
        eventos = EventoRepository.filtrar_eventos(categoria, busca)
        return [e.to_dict() for e in eventos]

    @staticmethod
    def obter_detalhe_evento(slug, ano_filtro=None):
        evento = EventoRepository.buscar_por_slug(slug)
        evento_dict = evento.to_dict()

        edicoes = evento_dict.get("edicoes", [])
        if ano_filtro:
            edicoes = [e for e in edicoes if str(e.get("ano")) == str(ano_filtro)]

        anos = sorted({e.get("ano") for e in evento_dict.get("edicoes", [])}, reverse=True)
        relacionados = [e.to_dict() for e in EventoRepository.buscar_relacionados(slug, 3)]

        return evento_dict, edicoes, anos, relacionados

    @staticmethod
    def criar_evento(nome, categoria, introducao, alinhamento, texto_secundario, banner_file, banner_url, corpo_file, corpo_url):
        slug = re.sub(r'-+', '-', re.sub(r'[^a-zA-Z0-9]', '-', nome.lower())).strip('-')

        banner = UploadService.salvar_imagem(banner_file, banner_url)
        corpo = UploadService.salvar_imagem(corpo_file, corpo_url, nome_padrao='')

        evento = Evento(
            slug=slug,
            nome=nome,
            categoria=categoria,
            banner=banner,
            introducao=introducao,
            imagem_corpo=corpo,
            alinhamento=alinhamento,
            texto_secundario=texto_secundario
        )
        EventoRepository.salvar(evento)

    @staticmethod
    def editar_evento(id, nome, categoria, introducao, alinhamento, texto_secundario, banner_file, banner_url, corpo_file, corpo_url):
        evento = EventoRepository.buscar_por_id(id)
        
        evento.nome = nome
        evento.categoria = categoria
        evento.introducao = introducao
        evento.alinhamento = alinhamento
        evento.texto_secundario = texto_secundario

        # Atualiza a imagem apenas se o usuário enviou uma nova
        if (banner_file and banner_file.filename != '') or banner_url:
            evento.banner = UploadService.salvar_imagem(banner_file, banner_url, nome_padrao=evento.banner)
            
        if (corpo_file and corpo_file.filename != '') or corpo_url:
            evento.imagem_corpo = UploadService.salvar_imagem(corpo_file, corpo_url, nome_padrao=evento.imagem_corpo)
            
        EventoRepository.sa_alteracao_direta()

    @staticmethod
    def deletar_evento(id):
        evento = EventoRepository.buscar_por_id(id)
        EventoRepository.deletar(evento)