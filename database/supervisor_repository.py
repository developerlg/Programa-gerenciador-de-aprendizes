from datetime import datetime

from database.conexao import obter_conexao
from models.supervisor import Supervisor


class SupervisorRepository:
    def criar(self, supervisor: Supervisor) -> int:
        with obter_conexao() as conexao:
            cursor = conexao.execute(
                """
                INSERT INTO supervisores (
                    nome,
                    funcao,
                    setor,
                    ativo,
                    data_atualizacao
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    supervisor.nome,
                    supervisor.funcao,
                    supervisor.setor,
                    int(supervisor.ativo),
                    supervisor.data_atualizacao,
                ),
            )
            return int(cursor.lastrowid)

    def atualizar(self, supervisor: Supervisor) -> None:
        with obter_conexao() as conexao:
            conexao.execute(
                """
                UPDATE supervisores
                   SET nome = ?,
                       funcao = ?,
                       setor = ?,
                       ativo = ?,
                       data_atualizacao = ?
                 WHERE id = ?
                """,
                (
                    supervisor.nome,
                    supervisor.funcao,
                    supervisor.setor,
                    int(supervisor.ativo),
                    supervisor.data_atualizacao,
                    supervisor.id,
                ),
            )

    def listar(self, termo: str = "") -> list[Supervisor]:
        termo = termo.strip()
        parametros: tuple[str, ...] = ()
        filtro = ""

        if termo:
            like = f"%{termo}%"
            parametros = (like, like, like)
            filtro = """
                WHERE nome LIKE ?
                   OR funcao LIKE ?
                   OR setor LIKE ?
            """

        with obter_conexao() as conexao:
            linhas = conexao.execute(
                f"""
                SELECT *
                  FROM supervisores
                {filtro}
                 ORDER BY nome
                """,
                parametros,
            ).fetchall()
            return [Supervisor.from_row(linha) for linha in linhas]

    def listar_ativos(self) -> list[Supervisor]:
        with obter_conexao() as conexao:
            linhas = conexao.execute(
                """
                SELECT *
                  FROM supervisores
                 WHERE ativo = 1
                 ORDER BY nome
                """
            ).fetchall()
            return [Supervisor.from_row(linha) for linha in linhas]

    def obter_por_id(self, supervisor_id: int) -> Supervisor | None:
        with obter_conexao() as conexao:
            linha = conexao.execute(
                """
                SELECT *
                  FROM supervisores
                 WHERE id = ?
                """,
                (supervisor_id,),
            ).fetchone()
            return Supervisor.from_row(linha) if linha else None

    def nome_existe(self, nome: str, ignorar_id: int | None = None) -> bool:
        parametros: list = [nome]
        filtro = ""
        if ignorar_id is not None:
            filtro = "AND id <> ?"
            parametros.append(ignorar_id)

        with obter_conexao() as conexao:
            linha = conexao.execute(
                f"""
                SELECT 1
                  FROM supervisores
                 WHERE nome = ?
                {filtro}
                 LIMIT 1
                """,
                tuple(parametros),
            ).fetchone()
            return linha is not None

    def contar_ativos(self) -> int:
        with obter_conexao() as conexao:
            linha = conexao.execute(
                """
                SELECT COUNT(*) AS total
                  FROM supervisores
                 WHERE ativo = 1
                """
            ).fetchone()
            return int(linha["total"])

    def atualizar_ativo(self, supervisor_id: int, ativo: bool) -> None:
        with obter_conexao() as conexao:
            conexao.execute(
                """
                UPDATE supervisores
                   SET ativo = ?,
                       data_atualizacao = ?
                 WHERE id = ?
                """,
                (
                    int(ativo),
                    datetime.now().isoformat(timespec="seconds"),
                    supervisor_id,
                ),
            )
