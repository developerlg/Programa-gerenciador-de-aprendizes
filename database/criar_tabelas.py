from config import DATABASE_PATH
from database.conexao import obter_conexao


SUPERVISORES_LEGADOS = (
    "Luis Henrique",
    "Vanessa Souza",
    "Luis Gustavo",
)


def inicializar_banco():
    with obter_conexao() as conexao:
        _preparar_supervisores(conexao)
        _preparar_aprendizes(conexao)
        _preparar_atividades(conexao)
        _criar_indices(conexao)
        _remover_supervisores_legados(conexao)

    return DATABASE_PATH


def _preparar_supervisores(conexao):
    if not _tabela_existe(conexao, "supervisores"):
        conexao.execute(
            """
            CREATE TABLE supervisores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                funcao TEXT NOT NULL DEFAULT '',
                setor TEXT NOT NULL DEFAULT '',
                ativo INTEGER NOT NULL DEFAULT 1,
                criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                data_atualizacao TEXT
            )
            """
        )
        return

    colunas = _colunas(conexao, "supervisores")
    if "funcao" not in colunas:
        conexao.execute("ALTER TABLE supervisores ADD COLUMN funcao TEXT NOT NULL DEFAULT ''")
    if "setor" not in colunas:
        conexao.execute("ALTER TABLE supervisores ADD COLUMN setor TEXT NOT NULL DEFAULT ''")
    if "data_atualizacao" not in colunas:
        conexao.execute("ALTER TABLE supervisores ADD COLUMN data_atualizacao TEXT")


def _preparar_aprendizes(conexao):
    if not _tabela_existe(conexao, "aprendizes"):
        _criar_tabela_aprendizes(conexao)
        return

    colunas = _colunas(conexao, "aprendizes")
    if {"nome", "cpf", "supervisor_id", "observacao", "ativo"}.issubset(colunas):
        return

    _criar_tabela_aprendizes(conexao, nome="aprendizes_v11")

    nome_expr = "nome" if "nome" in colunas else "nome_completo"
    cpf_expr = "cpf" if "cpf" in colunas else "''"
    setor_expr = "setor" if "setor" in colunas else "''"
    observacao_expr = "observacao" if "observacao" in colunas else "''"
    if "observacoes" in colunas:
        observacao_expr = "observacoes"
    ativo_expr = "ativo" if "ativo" in colunas else "CASE WHEN status = 'Inativo' THEN 0 ELSE 1 END"
    data_cadastro_expr = "data_cadastro" if "data_cadastro" in colunas else "date('now')"
    data_atualizacao_expr = "data_atualizacao" if "data_atualizacao" in colunas else "NULL"

    if "supervisor_id" in colunas:
        supervisor_expr = "supervisor_id"
    elif "supervisor_responsavel" in colunas:
        supervisor_expr = """
            (
                SELECT id
                  FROM supervisores
                 WHERE supervisores.nome = aprendizes.supervisor_responsavel
                 LIMIT 1
            )
        """
    else:
        supervisor_expr = "NULL"

    conexao.execute(
        f"""
        INSERT INTO aprendizes_v11 (
            id,
            nome,
            cpf,
            setor,
            observacao,
            supervisor_id,
            ativo,
            data_cadastro,
            data_atualizacao
        )
        SELECT
            id,
            COALESCE(NULLIF({nome_expr}, ''), 'Sem nome'),
            COALESCE({cpf_expr}, ''),
            COALESCE({setor_expr}, ''),
            COALESCE({observacao_expr}, ''),
            {supervisor_expr},
            COALESCE({ativo_expr}, 1),
            COALESCE({data_cadastro_expr}, date('now')),
            {data_atualizacao_expr}
          FROM aprendizes
        """
    )
    conexao.execute("DROP TABLE aprendizes")
    conexao.execute("ALTER TABLE aprendizes_v11 RENAME TO aprendizes")


def _preparar_atividades(conexao):
    conexao.execute(
        """
        CREATE TABLE IF NOT EXISTS atividades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aprendiz_id INTEGER NOT NULL,
            atividade_executada TEXT NOT NULL,
            descricao TEXT,
            observacao TEXT,
            prazo_estimado TEXT,
            data_cadastro TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            data_atualizacao TEXT,
            FOREIGN KEY (aprendiz_id) REFERENCES aprendizes(id)
        )
        """
    )


def _criar_tabela_aprendizes(conexao, nome: str = "aprendizes"):
    conexao.execute(
        f"""
        CREATE TABLE {nome} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL DEFAULT '',
            setor TEXT,
            observacao TEXT,
            supervisor_id INTEGER,
            ativo INTEGER NOT NULL DEFAULT 1,
            data_cadastro TEXT NOT NULL,
            data_atualizacao TEXT,
            FOREIGN KEY (supervisor_id) REFERENCES supervisores(id)
        )
        """
    )


def _criar_indices(conexao):
    conexao.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_aprendizes_nome
        ON aprendizes (nome)
        """
    )
    conexao.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_aprendizes_cpf_unico
        ON aprendizes (cpf)
        WHERE cpf <> ''
        """
    )
    conexao.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_aprendizes_supervisor
        ON aprendizes (supervisor_id)
        """
    )
    conexao.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_atividades_aprendiz
        ON atividades (aprendiz_id)
        """
    )
    conexao.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_atividades_prazo
        ON atividades (prazo_estimado)
        """
    )


def _remover_supervisores_legados(conexao):
    placeholders = ", ".join("?" for _ in SUPERVISORES_LEGADOS)
    conexao.execute(
        f"""
        DELETE FROM supervisores
         WHERE nome IN ({placeholders})
           AND COALESCE(funcao, '') = ''
           AND id NOT IN (
                SELECT supervisor_id
                  FROM aprendizes
                 WHERE supervisor_id IS NOT NULL
           )
        """,
        SUPERVISORES_LEGADOS,
    )


def _tabela_existe(conexao, nome: str) -> bool:
    linha = conexao.execute(
        """
        SELECT 1
          FROM sqlite_master
         WHERE type = 'table'
           AND name = ?
        """,
        (nome,),
    ).fetchone()
    return linha is not None


def _colunas(conexao, tabela: str) -> set[str]:
    return {linha["name"] for linha in conexao.execute(f"PRAGMA table_info({tabela})")}
