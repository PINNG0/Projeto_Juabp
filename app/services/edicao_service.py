from app.repositories.edicao_repository import EdicaoRepository
from app.services.upload_service import UploadService
from app.models import Edicao, GaleriaLink


class EdicaoService:

    @staticmethod
    def obter_por_evento(evento_id):
        return EdicaoRepository.obter_por_evento(evento_id)

    @staticmethod
    def criar_edicao(
        evento_id,
        ano,
        tema,
        local,
        descricao,
        capa_file,
        capa_url,
        link_nomes,
        link_urls
    ):
        capa = UploadService.salvar_imagem(capa_file, capa_url)

        edicao = Edicao(
            evento_id=evento_id,
            ano=ano,
            tema=tema,
            local=local,
            descricao=descricao,
            imagem_capa=capa
        )

        EdicaoRepository.salvar(edicao)

        for nome, url in zip(link_nomes, link_urls):
            if nome.strip() and url.strip():
                link = GaleriaLink(
                    edicao_id=edicao.id,
                    nome=nome.strip(),
                    url=url.strip()
                )
                EdicaoRepository.adicionar_relacionado(link)

    @staticmethod
    def deletar_edicao(id):
        edicao = EdicaoRepository.sa_objeto_id(id)
        EdicaoRepository.deletar(edicao)