import re
from app.repositories.evento_repository import EventoRepository
from app.services.upload_service import UploadService
from app.utils.evento_mapper import EventoMapper
from app.models import Evento

class EventoService:
    @staticmethod
    def obter_home_eventos():
        return [EventoMapper.evento_para_dict(e) for e in EventoRepository.obter_limite(6)]

    @staticmethod
    def obter_categorias():
        return EventoRepository.obter_categorias()

    @staticmethod
    def listar_eventos(categoria=None, busca=None):
        return [EventoMapper.evento_para_dict(e) for e in EventoRepository.filtrar_eventos(categoria, busca)]

    @staticmethod
    def obter_detalhe_evento(slug, ano_filtro=None):
        evento_bd = EventoRepository.buscar_por_slug(slug)
        evento_dict = EventoMapper.evento_para_dict(evento_bd)
        
        edicoes = evento_dict.get('edicoes', [])
        if ano_filtro:
            edicoes = [ed for ed in edicoes if str(ed.get('ano')) == ano_filtro]
            
        anos = sorted({ed.get('ano') for ed in evento_dict.get('edicoes', [])}, reverse=True)
        relacionados = [EventoMapper.evento_para_dict(e) for e in EventoRepository.buscar_relacionados(slug, 3)]
        
        return evento_dict, edicoes, anos, relacionados

    @staticmethod
    def criar_evento(nome, categoria, introducao, alinhamento, texto_secundario, banner_file, banner_url, corpo_file, corpo_url):
        slug = re.sub(r'-+', '-', re.sub(r'[^a-zA-Z0-9]', '-', nome.lower())).strip('-')
        nome_banner = UploadService.salvar_imagem(banner_file, banner_url)
        nome_corpo = UploadService.salvar_imagem(corpo_file, corpo_url, nome_padrao='')
        
        desc_json = EventoMapper.empacotar_json(introducao, nome_corpo, alinhamento, texto_secundario)
        novo_evento = Evento(slug=slug, nome=nome, descricao=desc_json, banner=nome_banner, categoria=categoria)
        EventoRepository.salvar(novo_evento)

    @staticmethod
    def editar_evento(id, nome, categoria):
        evento = EventoRepository.buscar_por_id(id)
        evento.nome = nome
        evento.categoria = categoria
        EventoRepository.sa_alteracao_direta()

    @staticmethod
    def deletar_evento(id):
        EventoRepository.deletar(EventoRepository.buscar_por_id(id))