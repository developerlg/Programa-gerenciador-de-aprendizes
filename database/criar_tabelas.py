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
    if _schema_aprendizes_atual(colunas):
        return

    _criar_tabela_aprendizes(conexao, nome="aprendizes_v13")

    nome_expr = "nome" if "nome" in colunas else "nome_completo"
    cpf_expr = "cpf" if "cpf" in colunas else "''"
    setor_expr = "setor" if "setor" in colunas else "''"
    observacao_expr = "observacao" if "observacao" in colunas else "''"
    if "observacoes" in colunas:
        observacao_expr = "observacoes"
    ativo_expr = "ativo" if "ativo" in colunas else "CASE WHEN status = 'Inativo' THEN 0 ELSE 1 END"
    data_cadastro_expr = "data_cadastro" if "data_cadastro" in colunas else "date('now')"
    data_atualizacao_expr = "data_atualizacao" if "data_atualizacao" in colunas else "NULL"

    conexao.execute(
        f"""
        INSERT INTO aprendizes_v13 (
            id,
            nome,
            cpf,
            setor,
            observacao,
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
            COALESCE({ativo_expr}, 1),
            COALESCE({data_cadastro_expr}, date('now')),
            {data_atualizacao_expr}
          FROM aprendizes
        """
    )
    conexao.execute("DROP TABLE aprendizes")
    conexao.execute("ALTER TABLE aprendizes_v13 RENAME TO aprendizes")


def _preparar_atividades(conexao):
    if not _tabela_existe(conexao, "atividades"):
        _criar_tabela_atividades(conexao)
        return

    colunas = _colunas(conexao, "atividades")
    if _schema_atividades_atual(colunas):
        return

    _criar_tabela_atividades(conexao, nome="atividades_v13")

    aprendiz_expr = "aprendiz_id" if "aprendiz_id" in colunas else "NULL"
    supervisor_expr = "supervisor_id" if "supervisor_id" in colunas else "NULL"
    atividade_expr = "atividade_executada" if "atividade_executada" in colunas else "''"
    descricao_expr = "descricao" if "descricao" in colunas else "''"
    observacao_expr = "observacao" if "observacao" in colunas else "''"
    prazo_expr = "prazo_estimado" if "prazo_estimado" in colunas else "''"
    data_cadastro_expr = "data_cadastro" if "data_cadastro" in colunas else "datetime('now')"
    data_atualizacao_expr = "data_atualizacao" if "data_atualizacao" in colunas else "NULL"

    conexao.execute(
        f"""
        INSERT INTO atividades_v13 (
            id,
            aprendiz_id,
            supervisor_id,
            atividade_executada,
            descricao,
            observacao,
            prazo_estimado,
            data_cadastro,
            data_atualizacao
        )
        SELECT
            id,
            {aprendiz_expr},
            {supervisor_expr},
            COALESCE(NULLIF({atividade_expr}, ''), 'Atividade sem titulo'),
            COALESCE({descricao_expr}, ''),
            COALESCE({observacao_expr}, ''),
            COALESCE({prazo_expr}, ''),
            COALESCE({data_cadastro_expr}, datetime('now')),
            {data_atualizacao_expr}
          FROM atividades
         WHERE {aprendiz_expr} IS NOT NULL
        """
    )
    conexao.execute("DROP TABLE atividades")
    conexao.execute("ALTER TABLE atividades_v13 RENAME TO atividades")


def _criar_tabela_aprendizes(conexao, nome: str = "aprendizes"):
    conexao.execute(
        f"""
        CREATE TABLE {nome} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL DEFAULT '',
            setor TEXT,
            observacao TEXT,
            ativo INTEGER NOT NULL DEFAULT 1,
            data_cadastro TEXT NOT NULL,
            data_atualizacao TEXT
        )
        """
    )


def _criar_tabela_atividades(conexao, nome: str = "atividades"):
    conexao.execute(
        f"""
        CREATE TABLE {nome} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aprendiz_id INTEGER NOT NULL,
            supervisor_id INTEGER,
            atividade_executada TEXT NOT NULL,
            descricao TEXT,
            observacao TEXT,
            prazo_estimado TEXT,
            data_cadastro TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            data_atualizacao TEXT,
            FOREIGN KEY (aprendiz_id) REFERENCES aprendizes(id),
            FOREIGN KEY (supervisor_id) REFERENCES supervisores(id)
        )
        """
    )


def _criar_indices(conexao):
    conexao.execute("DROP INDEX IF EXISTS idx_aprendizes_supervisor")
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
        CREATE INDEX IF NOT EXISTS idx_atividades_aprendiz
        ON atividades (aprendiz_id)
        """
    )
    conexao.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_atividades_supervisor
        ON atividades (supervisor_id)
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
           AND COALESCE(setor, '') = ''
        """,
        SUPERVISORES_LEGADOS,
    )


def _schema_aprendizes_atual(colunas: set[str]) -> bool:
    obrigatorias = {
        "nome",
        "cpf",
        "setor",
        "observacao",
        "ativo",
        "data_cadastro",
        "data_atualizacao",
    }
    return obrigatorias.issubset(colunas) and "supervisor_id" not in colunas


def _schema_atividades_atual(colunas: set[str]) -> bool:
    obrigatorias = {
        "aprendiz_id",
        "supervisor_id",
        "atividade_executada",
        "descricao",
        "observacao",
        "prazo_estimado",
        "data_cadastro",
        "data_atualizacao",
    }
    return obrigatorias.issubset(colunas)


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
