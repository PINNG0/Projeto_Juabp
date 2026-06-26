from app.repositories.inscricao_repository import InscricaoRepository
from app.models import Inscricao
from app.utils.notifier import Notifier 

class InscricaoService:
    @staticmethod
    def obter_todas():
        return InscricaoRepository.obter_todas()

    @staticmethod
    def criar_inscricao(nome, telefone, cidade, mensagem, ip_origem):
        nova_inscricao = Inscricao(
            nome=nome,
            telefone=telefone,
            cidade=cidade,
            mensagem=mensagem,
            ip_origem=ip_origem,
            termo_aceite=True
        )
        # 1. Salva no banco de dados
        InscricaoRepository.salvar(nova_inscricao)

        # 2. Monta a mensagem e dispara para o celular
        texto_alerta = (
            f"🚨 <b>NOVA INSCRIÇÃO - JUABP</b>\n\n"
            f"👤 <b>Nome:</b> {nome}\n"
            f"📍 <b>Cidade:</b> {cidade}\n"
            f"📱 <b>WhatsApp:</b> {telefone}\n"
        )
        Notifier.enviar_alerta_telegram(texto_alerta)

    @staticmethod
    def deletar_inscricao(id):
        inscricao = InscricaoRepository.buscar_por_id(id)
        InscricaoRepository.deletar(inscricao)