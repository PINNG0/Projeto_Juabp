from main import app
from database import db
from models import Usuario

with app.app_context():
    # 1. Cria todas as tabelas novas baseadas no models.py
    db.create_all()

    # 2. Verifica se já existe um administrador para não duplicar
    admin_existe = Usuario.query.filter_by(username='diretoria').first()
    
    if not admin_existe:
        # 3. Cria o usuário e criptografa a senha na mesma hora
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
        print("⚠️ O administrador já existe no banco de dados.")