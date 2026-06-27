import os

BASE_DIR = os.path.abspath(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)
        )
    )
)

INSTANCE_DIR = os.path.join(BASE_DIR, "instance")


class Config:
    # 🔐 SECRET KEY com fallback seguro para DEV
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev_key_insegura_123")

    # Banco de dados
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        INSTANCE_DIR,
        "juabp.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Uploads (opcional, mas evita crash futuro)
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    UPLOAD_ALLOWED_EXTENSIONS = "png,jpg,jpeg,webp,gif"