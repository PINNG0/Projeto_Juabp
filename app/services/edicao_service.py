from app.repositories.edicao_repository import EdicaoRepository
from app.services.upload_service import UploadService
from app.models import Edicao, GaleriaLink

class EdicaoService:
    @staticmethod
    def obter_por_evento(evento_id):
        return EdicaoRepository.obter_por_evento(evento_id)

    @staticmethod
    def criar_edicao(evento_id, ano, tema, local, descricao, capa_file, capa_url, link_nomes, link_urls):
        nome_capa = UploadService.salvar_imagem(capa_file, capa_url)
        nova_edicao = Edicao(
            evento_id=evento_id, ano=ano, tema=tema, local=local, 
            descricao=descricao, imagem_capa=nome_capa
        )
        EdicaoRepository.salvar(nova_edicao)
        
        for nome, url in zip(link_nomes, link_urls):
            if nome.strip() and url.strip():
                novo_link = GaleriaLink(edicao_id=nova_edicao.id, nome=nome.strip(), url=url.strip())
                EdicaoRepository.adicionar_relacionado(novo_link)

    @staticmethod
    def deletar_edicao(id):
        EdicaoRepository.deletar(EdicaoRepository.sa_objeto_id(id))