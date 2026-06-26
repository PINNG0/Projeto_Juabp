import requests

class InstagramService:
    @staticmethod
    def get_recent_posts():
        # Por enquanto, estamos em modo de "mock" (simulação)
        # Quando você tiver o Token da Meta, preencheremos aqui.
        
        # Estrutura que o site espera receber:
        return [
            {"image": "static/img/juabp_post1.jpg", "caption": "Ensaio Geral!", "url": "#"},
            {"image": "static/img/juabp_post2.jpg", "caption": "Bastidores 2026", "url": "#"}
        ]

        # ROTEIRO FUTURO (Quando tiver o Token):
        # 1. token = "SEU_TOKEN_AQUI"
        # 2. response = requests.get(f"https://graph.instagram.com/me/media?fields=media_url,caption,permalink&access_token={token}")
        # 3. Processar o JSON e retornar a lista.