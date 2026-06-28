from app.database.database import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Usuario(db.Model):
    __tablename__ = "usuarios"

    # ==========================================
    # IDENTIFICAÇÃO
    # ==========================================
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(256),
        nullable=True
    )

    # ==========================================
    # LOGIN SOCIAL
    # ==========================================
    google_id = db.Column(
        db.String(200),
        unique=True,
        nullable=True
    )

    auth_provider = db.Column(
        db.String(20),
        default='local'
    )  # local | google

    # ==========================================
    # DADOS PESSOAIS
    # ==========================================
    nome_completo = db.Column(
        db.String(100),
        nullable=True
    )

    data_nascimento = db.Column(
        db.Date,
        nullable=True
    )

    telefone = db.Column(
        db.String(20),
        nullable=True
    )

    cidade = db.Column(
        db.String(100),
        nullable=True
    )

    estado = db.Column(
        db.String(100),
        nullable=True
    )

    # ==========================================
    # PERFIL
    # ==========================================
    biografia = db.Column(
        db.String(255),
        nullable=True
    )

    # Caminho local ou URL completa
    foto_perfil = db.Column(
        db.String(500),
        default='default_perfil.png'
    )

    instagram_link = db.Column(
        db.String(150),
        nullable=True
    )

    facebook_link = db.Column(
        db.String(150),
        nullable=True
    )

    tiktok_link = db.Column(
        db.String(150),
        nullable=True
    )

    site_pessoal = db.Column(
        db.String(255),
        nullable=True
    )

    # ==========================================
    # SISTEMA
    # ==========================================
    cargo = db.Column(
        db.String(20),
        default='visitante'
    )

    status = db.Column(
        db.String(20),
        default='ativo'
    )

    email_verificado = db.Column(
        db.Boolean,
        default=False
    )

    data_criacao = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    ultimo_login = db.Column(
        db.DateTime,
        nullable=True
    )

    # ==========================================
    # MÉTODOS
    # ==========================================
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if not self.password_hash:
            return False

        return check_password_hash(
            self.password_hash,
            password
        )

    def is_admin(self):
        return self.cargo == 'diretoria'

    @property
    def avatar(self):
        """
        Retorna a foto do usuário.
        Funciona tanto para URL externa quanto para arquivo local.
        """
        return self.foto_perfil or 'default_perfil.png'

    def __repr__(self):
        return f"<Usuario {self.username}>"