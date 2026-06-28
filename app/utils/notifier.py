import os
import requests

class Notifier:

    @staticmethod
    def enviar_alerta_telegram(mensagem):
        # Agora ele puxa do arquivo .env com segurança!
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')

        if not bot_token or not chat_id:
            print("\n" + "=" * 40)
            print("📲 ALERTA (SIMULAÇÃO - Telegram não configurado no .env)")
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
            pass