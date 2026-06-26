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
        novo_admin = Usuario(username='diretoria')
        novo_admin.set_password('@Tsunami2026') 
        
        db.session.add(novo_admin)
        db.session.commit()
        
        print("\n====================================")
        print("✅ BANCO DE DADOS ATUALIZADO!")
        print("👤 Login criado: diretoria")
        print("🔑 Senha: @Tsunami2026")
        print("====================================\n")
    else:
        # Se já existir e estiver dando erro, força a atualização da senha
        admin_existe.set_password('@Tsunami2026')
        db.session.commit()
        print("\n====================================")
        print("🔄 SENHA DO ADMIN REDEFINIDA COM SUCESSO!")
        print("👤 Login: diretoria")
        print("🔑 Senha: @Tsunami2026")
        print("====================================\n")