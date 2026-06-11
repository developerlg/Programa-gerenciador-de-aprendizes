from config import DATABASE_PATH
from database.conexao import obter_conexao


SUPERVISORES_INICIAIS = (
    "Luis Henrique",
    "Vanessa Souza",
    "Luis Gustavo",
)


def inicializar_banco():
    with obter_conexao() as conexao:
        conexao.execute(
            """
            CREATE TABLE IF NOT EXISTS supervisores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                ativo INTEGER NOT NULL DEFAULT 1,
                criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conexao.execute(
            """
            CREATE TABLE IF NOT EXISTS aprendizes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_completo TEXT NOT NULL,
                supervisor_responsavel TEXT NOT NULL,
                data_nascimento TEXT,
                data_admissao TEXT,
                setor TEXT,
                observacoes TEXT,
                status TEXT NOT NULL DEFAULT 'Ativo',
                data_cadastro TEXT NOT NULL,
                data_atualizacao TEXT
            )
            """
        )
        conexao.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_aprendizes_nome
            ON aprendizes (nome_completo)
            """
        )
        conexao.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_aprendizes_status
            ON aprendizes (status)
            """
        )
        conexao.executemany(
            """
            INSERT OR IGNORE INTO supervisores (nome)
            VALUES (?)
            """,
            [(nome,) for nome in SUPERVISORES_INICIAIS],
        )

    return DATABASE_PATH
