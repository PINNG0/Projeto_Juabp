import os

# Define a raiz do projeto (Projeto_Juabp)
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'chave_secreta_super_segura_aqui')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(INSTANCE_DIR, "juabp.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False