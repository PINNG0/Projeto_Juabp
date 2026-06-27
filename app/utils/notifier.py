import requests


class Notifier:

    @staticmethod
    def enviar_alerta_telegram(mensagem):
        bot_token = 'SEU_TOKEN_AQUI'
        chat_id = 'SEU_CHAT_ID_AQUI'

        if bot_token == 'SEU_TOKEN_AQUI':
            print("\n" + "=" * 40)
            print("📲 ALERTA (SIMULAÇÃO)")
            print("=" * 40)
            print(mensagem.replace('<b>', '').replace('</b>', ''))
            print("=" * 40 + "\n")
            return

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

        payload = {
            'chat_id': chat_id,
            'text': mensagem,
            'parse_mode': 'HTML'
        }

        try:
            requests.post(url, json=payload, timeout=5)
        except Exception:
            # não quebra fluxo do usuário
            pass