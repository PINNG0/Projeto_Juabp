import re
from app.repositories.evento_repository import EventoRepository
from app.services.upload_service import UploadService
from app.utils.evento_mapper import EventoMapper
from app.models import Evento


class EventoService:

    @staticmethod
    def obter_home_eventos():
        eventos = EventoRepository.obter_limite(6)
        return [EventoMapper.evento_para_dict(e) for e in eventos]

    @staticmethod
    def obter_categorias():
        return EventoRepository.obter_categorias()

    @staticmethod
    def listar_eventos(categoria=None, busca=None):
        eventos = EventoRepository.filtrar_eventos(categoria, busca)
        return [EventoMapper.evento_para_dict(e) for e in eventos]

    @staticmethod
    def obter_detalhe_evento(slug, ano_filtro=None):
        evento = EventoRepository.buscar_por_slug(slug)
        evento_dict = EventoMapper.evento_para_dict(evento)

        edicoes = evento_dict.get("edicoes", [])

        if ano_filtro:
            edicoes = [
                e for e in edicoes
                if str(e.get("ano")) == str(ano_filtro)
            ]

        anos = sorted(
            {e.get("ano") for e in evento_dict.get("edicoes", [])},
            reverse=True
        )

        relacionados = [
            EventoMapper.evento_para_dict(e)
            for e in EventoRepository.buscar_relacionados(slug, 3)
        ]

        return evento_dict, edicoes, anos, relacionados

    @staticmethod
    def criar_evento(
        nome,
        categoria,
        introducao,
        alinhamento,
        texto_secundario,
        banner_file,
        banner_url,
        corpo_file,
        corpo_url
    ):
        slug = re.sub(
            r'-+',
            '-',
            re.sub(r'[^a-zA-Z0-9]', '-', nome.lower())
        ).strip('-')

        banner = UploadService.salvar_imagem(banner_file, banner_url)
        corpo = UploadService.salvar_imagem(corpo_file, corpo_url, nome_padrao='')

        descricao = EventoMapper.empacotar_json(
            introducao,
            corpo,
            alinhamento,
            texto_secundario
        )

        evento = Evento(
            slug=slug,
            nome=nome,
            categoria=categoria,
            descricao=descricao,
            banner=banner
        )

        EventoRepository.salvar(evento)

    @staticmethod
    def editar_evento(id, nome, categoria):
        evento = EventoRepository.buscar_por_id(id)
        evento.nome = nome
        evento.categoria = categoria
        EventoRepository.sa_alteracao_direta()

    @staticmethod
    def deletar_evento(id):
        evento = EventoRepository.buscar_por_id(id)
        EventoRepository.deletar(evento)