import os
from flask import Flask
from app.database.database import db
from app.config.config import Config, INSTANCE_DIR

def create_app():
    app = Flask(__name__)
    
    # Carrega as configurações limpas
    app.config.from_object(Config)

    if not os.path.exists(INSTANCE_DIR):
        os.makedirs(INSTANCE_DIR)

    db.init_app(app)

    # Importa os modelos centralizados (AvisoInterno adicionado aqui)
    from app.models import Usuario, Evento, Edicao, GaleriaLink, Inscricao, AvisoInterno

    with app.app_context():
        db.create_all()

    # Registra as rotas
    from app.routes.public_routes import public_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.admin_routes import admin_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    return app