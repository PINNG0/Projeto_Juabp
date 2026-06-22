from main import app
from database import db
from models import Evento, Edicao, GaleriaLink
from data.eventos import eventos

with app.app_context():
    print("\n====================================")
    print("🔄 INICIANDO MIGRAÇÃO DE EVENTOS...")
    
    eventos_migrados = 0

    for ev_data in eventos:
        # Verifica se o evento já foi migrado para não duplicar
        evento_existente = Evento.query.filter_by(slug=ev_data['slug']).first()
        
        if evento_existente:
            print(f"⚠️ Evento '{ev_data['nome']}' já existe. Pulando...")
            continue

        # 1. Cria o Evento Principal (Usa .get() para evitar quebra se faltar algum dado)
        novo_evento = Evento(
            slug=ev_data.get('slug'),
            nome=ev_data.get('nome'),
            descricao=ev_data.get('descricao', 'Sem descrição.'),
            banner=ev_data.get('banner', 'campea.jpeg'), # Imagem padrão se não houver
            categoria=ev_data.get('categoria', 'Geral')
        )
        db.session.add(novo_evento)
        db.session.flush() # Salva temporariamente para gerar o ID do evento

        # 2. Migra as Edições do evento (se existirem)
        if 'edicoes' in ev_data:
            for ed_data in ev_data['edicoes']:
                nova_edicao = Edicao(
                    evento_id=novo_evento.id,
                    ano=ed_data.get('ano', 2026),
                    tema=ed_data.get('tema', 'Tema não informado'),
                    local=ed_data.get('local', 'Local a definir'),
                    descricao=ed_data.get('descricao', ''),
                    # Aqui estava o erro! Agora ele coloca 'campea.jpeg' se não achar a capa
                    imagem_capa=ed_data.get('imagem_capa', 'campea.jpeg') 
                )
                db.session.add(nova_edicao)
                db.session.flush() # Salva temporariamente para gerar o ID da edição

                # 3. Migra os Links de Galeria da edição (se existirem)
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

    # Efetiva todas as gravações no banco de dados
    try:
        db.session.commit()
        print(f"\n🎉 MIGRAÇÃO CONCLUÍDA! {eventos_migrados} novos eventos inseridos.")
        print("====================================\n")
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ ERRO FATAL NO BANCO DE DADOS: {e}")
        print("====================================\n")