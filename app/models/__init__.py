# app/models/__init__.py
# Import central dos modelos usados pela aplicação.

from .usuario import Usuario
from .evento import Evento
from .edicao import Edicao
from .galeria_link import GaleriaLink
from .inscricao import Inscricao

# Aviso interno é opcional; não deve quebrar a inicialização se ausente.
try:
    from .aviso_interno import AvisoInterno  # type: ignore
    __all_extra__ = ["AvisoInterno"]
except Exception:
    AvisoInterno = None  # type: ignore
    __all_extra__ = []

__all__ = [
    "Usuario",
    "Evento",
    "Edicao",
    "GaleriaLink",
    "Inscricao",
] + __all_extra__
