import os
from werkzeug.utils import secure_filename
from flask import current_app

class UploadService:
    @staticmethod
    def salvar_imagem(arquivo_file, url_alternativa, nome_padrao='campea.jpeg'):
        """Verifica se há um arquivo para upload ou uma URL alternativa. Salva e retorna o nome final."""
        if arquivo_file and arquivo_file.filename:
            filename = secure_filename(arquivo_file.filename)
            caminho = os.path.join(current_app.static_folder, 'img', filename)
            arquivo_file.save(caminho)
            return filename
        elif url_alternativa:
            return url_alternativa.strip()
        
        return nome_padrao