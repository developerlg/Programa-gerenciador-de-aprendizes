import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from sqlite3 import Connection

from config import DATA_DIR, DATABASE_PATH


@contextmanager
def obter_conexao() -> Iterator[Connection]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
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
