import requests

class Notifier:
    @staticmethod
    def enviar_alerta_telegram(mensagem):
        # Chaves do Telegram (Deixe assim por enquanto)
        bot_token = 'SEU_TOKEN_AQUI' 
        chat_id = 'SEU_CHAT_ID_AQUI'
        
        # MODO DESENVOLVEDOR: Se não tem chave, avisa no terminal
        if bot_token == 'SEU_TOKEN_AQUI':
            print("\n" + "="*40)
            print("📲 ALERTA DE SISTEMA (Simulação de Celular)")
            print("="*40)
            # Limpa as tags <b> do HTML para o terminal ficar legível
            mensagem_limpa = mensagem.replace('<b>', '').replace('</b>', '')
            print(mensagem_limpa)
            print("="*40 + "\n")
            return 
            
        # MODO PRODUÇÃO: Quando você colocar a chave, o código abaixo assume o controle
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': mensagem,
            'parse_mode': 'HTML'
        }
        
        try:
            requests.post(url, json=payload, timeout=5)
        except Exception as e:
            # Erro silencioso para não travar a inscrição do usuário no site
            print(f"Erro silencioso ao enviar notificação: {e}")