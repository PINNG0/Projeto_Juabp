from app import create_app
from app.database.database import db
from app.models import Evento, Edicao, GaleriaLink
# Assumindo que o arquivo eventos.py esteja em app/data/eventos.py
from app.data.eventos import eventos 

# 1. Instanciamos a fábrica do app aqui!
app = create_app()

with app.app_context():
    print("\n====================================")
    print("🔄 INICIANDO MIGRAÇÃO DE EVENTOS...")
    
    eventos_migrados = 0

    for ev_data in eventos:
        evento_existente = Evento.query.filter_by(slug=ev_data['slug']).first()
        
        if evento_existente:
            print(f"⚠️ Evento '{ev_data.get('nome')}' já existe. Pulando...")
            continue

        novo_evento = Evento(
            slug=ev_data.get('slug'),
            nome=ev_data.get('nome'),
            descricao=ev_data.get('descricao', 'Sem descrição.'),
            banner=ev_data.get('banner', 'campea.jpeg'),
            categoria=ev_data.get('categoria', 'Geral')
        )
        db.session.add(novo_evento)
        db.session.flush()

        if 'edicoes' in ev_data:
            for ed_data in ev_data['edicoes']:
                nova_edicao = Edicao(
                    evento_id=novo_evento.id,
                    ano=ed_data.get('ano', 2026),
                    tema=ed_data.get('tema', 'Tema não informado'),
                    local=ed_data.get('local', 'Local a definir'),
                    descricao=ed_data.get('descricao', ''),
                    imagem_capa=ed_data.get('imagem_capa', 'campea.jpeg')
                )
                db.session.add(nova_edicao)
                db.session.flush()

                if 'links' in ed_data:
                    for link_data in ed_data['links']:
                        novo_link = GaleriaLink(
                            edicao_id=nova_edicao.id,
                            nome=link_data.get('nome', 'Galeria'),
                            url=link_data.get('url', '#')
                        )
                        db.session.add(novo_link)
        
        eventos_migrados += 1
        print(f"✅ Evento '{ev_data.get('nome')}' preparado.")

    try:
        db.session.commit()
        print(f"\n🎉 MIGRAÇÃO CONCLUÍDA! {eventos_migrados} novos eventos inseridos.")
        print("====================================\n")
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ ERRO FATAL: {e}")