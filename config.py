from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = DATA_DIR / "aprendizes.db"

APP_TITLE = "Sistema de Acompanhamento de Jovens Aprendizes"
APP_VERSION = "1.3.0"

CURRENT_USER_NAME = "Luis Gustavo"
CURRENT_USER_ROLE = "Supervisor"
