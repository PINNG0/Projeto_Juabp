import os
from app import create_app
from app.database.database import db
from app.models import Usuario, Evento, Edicao, GaleriaLink
from app.data.eventos import eventos

app = create_app()

def setup_database():
    with app.app_context():
        print("\n====================================")
        print("🔄 INICIANDO CONFIGURAÇÃO DO BANCO...")
        print("====================================")
        
        # 1. Cria todas as tabelas
        db.create_all()
        print("✅ Tabelas criadas/sincronizadas.")

        # 2. Configura o Admin (Puxando dados do ambiente, sem senhas no código!)
        admin_username = os.getenv('ADMIN_USERNAME', 'diretoria')
        admin_password = os.getenv('ADMIN_PASSWORD', 'MudeMe123!') 

        admin = Usuario.query.filter_by(username=admin_username).first()
        if not admin:
            admin = Usuario(
                username=admin_username,
                email='diretoria@juabp.com.br',
                cargo='diretoria',
                nome_completo='Diretoria JUABP'
            )
            admin.set_password(admin_password)
            db.session.add(admin)
            print(f"✅ Admin '{admin_username}' criado.")
        else:
            admin.set_password(admin_password)
            print(f"🔄 Admin '{admin_username}' atualizado com a senha atual.")

        # 3. Migrar Eventos (Importa apenas o que ainda não está no banco)
        eventos_migrados = 0
        for ev_data in eventos:
            if Evento.query.filter_by(slug=ev_data['slug']).first():
                continue # Ignora se já existe

            novo_evento = Evento(
            slug=ev_data.get('slug'),
                nome=ev_data.get('nome'),
                banner=ev_data.get('banner', 'campea.jpeg'),
                categoria=ev_data.get('categoria', 'Geral'),
                # Usamos a 'descricao' do dicionário antigo para preencher a 'introducao' nova
                introducao=ev_data.get('descricao', 'Sem descrição.')
            )
            db.session.add(novo_evento)
            db.session.flush()

            for ed_data in ev_data.get('edicoes', []):
                nova_edicao = Edicao(
                    evento_id=novo_evento.id,
                    ano=ed_data.get('ano', 2026),
                    tema=ed_data.get('tema', 'Tema não informado'),
                    local=ed_data.get('local', 'Local a definir'),
                    descricao=ed_data.get('descricao', ''),
                    imagem_capa=ed_data.get('imagem', 'campea.jpeg')
                )
                db.session.add(nova_edicao)
                db.session.flush()

                for link_data in ed_data.get('galerias_externas', []):
                    novo_link = GaleriaLink(
                        edicao_id=nova_edicao.id,
                        nome=link_data.get('nome', 'Galeria'),
                        url=link_data.get('url', '#')
                    )
                    db.session.add(novo_link)
            
            eventos_migrados += 1

        try:
            db.session.commit()
            print(f"✅ {eventos_migrados} novos eventos importados do dicionário.")
            print("\n🎉 BANCO DE DADOS 100% PRONTO!")
            print("====================================\n")
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ ERRO FATAL AO SALVAR: {e}")

if __name__ == '__main__':
    setup_database()