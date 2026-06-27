import os
from uuid import uuid4
from pathlib import Path

from werkzeug.utils import secure_filename
from flask import current_app

from PIL import Image, UnidentifiedImageError


class UploadService:

    DEFAULT_ALLOWED = {'png', 'jpg', 'jpeg', 'webp', 'gif'}
    DEFAULT_MAX_SIZE = 5 * 1024 * 1024  # 5MB

    @staticmethod
    def _allowed_extensions():
        cfg = current_app.config.get('UPLOAD_ALLOWED_EXTENSIONS')

        if cfg:
            return {x.strip().lower() for x in str(cfg).split(',')}

        return UploadService.DEFAULT_ALLOWED

    @staticmethod
    def _is_image_valid(path: Path):
        try:
            with Image.open(path) as img:
                img.verify()
            return True
        except (UnidentifiedImageError, OSError):
            return False

    @staticmethod
    def salvar_imagem(
        arquivo_file,
        url_alternativa=None,
        nome_padrao='campea.jpeg',
        max_size=None
    ):

        max_size = max_size or UploadService.DEFAULT_MAX_SIZE
        allowed = UploadService._allowed_extensions()

        # 1. Arquivo enviado
        if arquivo_file and getattr(arquivo_file, 'filename', None):

            filename = secure_filename(arquivo_file.filename)

            if '.' not in filename:
                raise ValueError('Arquivo inválido.')

            ext = filename.rsplit('.', 1)[-1].lower()

            if ext not in allowed:
                raise ValueError('Formato não permitido.')

            # valida tamanho
            try:
                arquivo_file.stream.seek(0, os.SEEK_END)
                size = arquivo_file.stream.tell()
                arquivo_file.stream.seek(0)
            except Exception:
                size = None

            if size and size > max_size:
                raise ValueError('Arquivo muito grande.')

            unique_name = f"{uuid4().hex}_{filename}"

            img_dir = Path(current_app.static_folder) / 'img'
            img_dir.mkdir(parents=True, exist_ok=True)

            file_path = img_dir / unique_name

            arquivo_file.save(str(file_path))

            # valida integridade real da imagem
            if not UploadService._is_image_valid(file_path):
                try:
                    file_path.unlink(missing_ok=True)
                except Exception:
                    pass
                raise ValueError('Imagem inválida ou corrompida.')

            return unique_name

        # 2. URL externa
        if url_alternativa:
            url = str(url_alternativa).strip()
            if url:
                return url

        # 3. fallback
        return nome_padrao