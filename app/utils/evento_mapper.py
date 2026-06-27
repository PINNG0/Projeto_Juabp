import json


class EventoMapper:

    @staticmethod
    def carregar_corpo_materia(descricao_str):
        if not descricao_str:
            return {
                'introducao': 'Sem descrição.',
                'imagem_corpo': '',
                'alinhamento': 'centro',
                'texto_secundario': ''
            }

        try:
            if descricao_str.strip().startswith('{'):
                return json.loads(descricao_str)
        except Exception:
            pass

        return {
            'introducao': descricao_str,
            'imagem_corpo': '',
            'alinhamento': 'centro',
            'texto_secundario': ''
        }

    @staticmethod
    def evento_para_dict(evento_obj):
        corpo = EventoMapper.carregar_corpo_materia(evento_obj.descricao)

        edicoes = []

        if hasattr(evento_obj, "edicoes"):
            try:
                edicoes = [
                    {
                        'id': ed.id,
                        'ano': ed.ano,
                        'tema': ed.tema,
                        'local': ed.local,
                        'descricao': ed.descricao,
                        'imagem_capa': ed.imagem_capa,
                        'links': [
                            {
                                'nome': lnk.nome,
                                'url': lnk.url
                            }
                            for lnk in getattr(ed, "galerias_externas", [])
                        ]
                    }
                    for ed in sorted(evento_obj.edicoes, key=lambda x: x.ano, reverse=True)
                ]
            except Exception:
                edicoes = []

        return {
            'id': evento_obj.id,
            'slug': evento_obj.slug,
            'nome': evento_obj.nome,
            'banner': evento_obj.banner,
            'categoria': evento_obj.categoria,

            'introducao': corpo.get('introducao', ''),
            'imagem_corpo': corpo.get('imagem_corpo', ''),
            'alinhamento': corpo.get('alinhamento', 'centro'),
            'texto_secundario': corpo.get('texto_secundario', ''),

            'edicoes': edicoes
        }

    @staticmethod
    def empacotar_json(introducao, imagem_corpo, alinhamento, texto_secundario):
        return json.dumps(
            {
                'introducao': introducao,
                'imagem_corpo': imagem_corpo,
                'alinhamento': alinhamento,
                'texto_secundario': texto_secundario
            },
            ensure_ascii=False
        )