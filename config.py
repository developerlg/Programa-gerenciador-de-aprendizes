import os
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
APP_SLUG = "ProgramaAprendizes"
INITIAL_DATABASE_NAME = "aprendizes_inicial.db"
RUNTIME_DATABASE_NAME = "aprendizes.db"


def executando_empacotado() -> bool:
    return bool(getattr(sys, "frozen", False))


def localizar_recurso(caminho_relativo: str | Path) -> Path:
    base = Path(getattr(sys, "_MEIPASS", BASE_DIR))
    return base / caminho_relativo


def _runtime_base_dir() -> Path:
    if not executando_empacotado():
        return BASE_DIR

    local_app_data = os.getenv("LOCALAPPDATA")
    if local_app_data:
        return Path(local_app_data) / APP_SLUG

    return Path.home() / "AppData" / "Local" / APP_SLUG


RESOURCE_DIR = localizar_recurso(".")
ASSETS_DIR = localizar_recurso("assets")
ICONS_DIR = ASSETS_DIR / "icons"
IMAGES_DIR = ASSETS_DIR / "imagens"
APP_ICON_PATH = ICONS_DIR / "app.ico"

RUNTIME_DIR = _runtime_base_dir()
DATA_DIR = RUNTIME_DIR / "data"
BACKUPS_DIR = RUNTIME_DIR / "backups"
REPORTS_DIR = RUNTIME_DIR / "reports"

BUNDLED_DATA_DIR = localizar_recurso("data")
BUNDLED_DATABASE_PATH = BUNDLED_DATA_DIR / INITIAL_DATABASE_NAME
DATABASE_PATH = DATA_DIR / RUNTIME_DATABASE_NAME


def garantir_pastas_execucao() -> None:
    for pasta in (DATA_DIR, BACKUPS_DIR, REPORTS_DIR):
        pasta.mkdir(parents=True, exist_ok=True)

APP_TITLE = "Sistema de Acompanhamento de Jovens Aprendizes"
APP_VERSION = "1.3.0"

CURRENT_USER_NAME = "Luis Gustavo"
CURRENT_USER_ROLE = "Supervisor"
