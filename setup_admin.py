import os
from app import create_app
from app.database.database import db
from app.models import Usuario

app = create_app()

ADMIN_USERNAME = os.getenv(
    'ADMIN_USERNAME',
    'diretoria'
)

ADMIN_PASSWORD = os.getenv(
    'ADMIN_PASSWORD',
    '@Tsunami2026'
)

with app.app_context():
    db.create_all()

    admin = Usuario.query.filter_by(
        username=ADMIN_USERNAME
    ).first()

    if not admin:
        admin = Usuario(
            username=ADMIN_USERNAME,
            cargo='diretoria'
        )

        admin.set_password(ADMIN_PASSWORD)

        db.session.add(admin)
        db.session.commit()

        print('\n====================================')
        print('✅ ADMIN CRIADO')
        print(f'👤 {ADMIN_USERNAME}')
        print('====================================\n')

    else:
        admin.cargo = 'diretoria'
        admin.set_password(ADMIN_PASSWORD)

        db.session.commit()

        print('\n====================================')
        print('🔄 ADMIN ATUALIZADO')
        print(f'👤 {ADMIN_USERNAME}')
        print('====================================\n')