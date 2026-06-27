from app import create_app
from app.database.database import db
from app.models import Usuario

# 1. Liga a nossa nova Fábrica de Aplicativos (o seu __init__.py)
app = create_app()

with app.app_context():
    # 2. Cria as tabelas no banco de dados novo
    db.create_all()

    # 3. Verifica se o admin existe
    admin_existe = Usuario.query.filter_by(username='diretoria').first()
    
    if not admin_existe:
        # ATUALIZADO: Agora criamos o usuário já com o cargo de 'diretoria'
        novo_admin = Usuario(username='diretoria', cargo='diretoria')
        novo_admin.set_password('@Tsunami2026') 
        
        db.session.add(novo_admin)
        db.session.commit()
        
        print("\n====================================")
        print("✅ BANCO DE DADOS ATUALIZADO!")
        print("👤 Login criado: diretoria")
        print("🔑 Senha: @Tsunami2026")
        print("🎖️ Cargo atribuído: diretoria")
        print("====================================\n")
    else:
        # ATUALIZADO: Se já existir, força a correção do cargo além da senha
        admin_existe.cargo = 'diretoria'
        admin_existe.set_password('@Tsunami2026')
        db.session.commit()
        
        print("\n====================================")
        print("🔄 ACESSO DO ADMIN ATUALIZADO COM SUCESSO!")
        print("👤 Login: diretoria")
        print("🔑 Senha: @Tsunami2026")
        print("🎖️ Cargo corrigido para: diretoria")
        print("====================================\n")