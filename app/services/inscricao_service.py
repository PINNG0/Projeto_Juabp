from app.repositories.inscricao_repository import InscricaoRepository
from app.models import Inscricao
from app.utils.notifier import Notifier


class InscricaoService:

    @staticmethod
    def obter_todas():
        return InscricaoRepository.obter_todas()

    @staticmethod
    def criar_inscricao(nome, telefone, cidade, mensagem, ip_origem):

        inscricao = Inscricao(
            nome=nome,
            telefone=telefone,
            cidade=cidade,
            mensagem=mensagem,
            ip_origem=ip_origem
        )

        InscricaoRepository.salvar(inscricao)

        Notifier.enviar_alerta_telegram(
            f"🚨 <b>NOVA INSCRIÇÃO - JUABP</b>\n\n"
            f"👤 <b>Nome:</b> {nome}\n"
            f"📍 <b>Cidade:</b> {cidade}\n"
            f"📱 <b>WhatsApp:</b> {telefone}\n"
        )

    @staticmethod
    def deletar_inscricao(id):
        inscricao = InscricaoRepository.buscar_por_id(id)
        InscricaoRepository.deletar(inscricao)