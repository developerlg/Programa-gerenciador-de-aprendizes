import sqlite3
import shutil
from collections.abc import Iterator
from contextlib import contextmanager
from sqlite3 import Connection

from config import BUNDLED_DATABASE_PATH, DATA_DIR, DATABASE_PATH


@contextmanager
def obter_conexao() -> Iterator[Connection]:
    _garantir_banco_runtime()
    conexao = sqlite3.connect(DATABASE_PATH)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    try:
        yield conexao
        conexao.commit()
    except Exception:
        conexao.rollback()
        raise
    finally:
        conexao.close()


def _garantir_banco_runtime() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if DATABASE_PATH.exists():
        return

    if not BUNDLED_DATABASE_PATH.exists():
        return

    if BUNDLED_DATABASE_PATH.resolve() == DATABASE_PATH.resolve():
        return

    shutil.copy2(BUNDLED_DATABASE_PATH, DATABASE_PATH)
