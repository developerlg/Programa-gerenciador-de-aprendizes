from datetime import datetime

from database.conexao import obter_conexao
from models.aprendiz import Aprendiz


class AprendizRepository:
    def criar(self, aprendiz: Aprendiz) -> int:
        with obter_conexao() as conexao:
            cursor = conexao.execute(
                """
                INSERT INTO aprendizes (
                    nome,
                    cpf,
                    setor,
                    observacao,
                    ativo,
                    data_cadastro,
                    data_atualizacao
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    aprendiz.nome,
                    aprendiz.cpf,
                    aprendiz.setor,
                    aprendiz.observacao,
                    int(aprendiz.ativo),
                    aprendiz.data_cadastro,
                    aprendiz.data_atualizacao,
                ),
            )
            return int(cursor.lastrowid)

    def atualizar(self, aprendiz: Aprendiz) -> None:
        with obter_conexao() as conexao:
            conexao.execute(
                """
                UPDATE aprendizes
                   SET nome = ?,
                       cpf = ?,
                       setor = ?,
                       observacao = ?,
                       ativo = ?,
                       data_atualizacao = ?
                 WHERE id = ?
                """,
                (
                    aprendiz.nome,
                    aprendiz.cpf,
                    aprendiz.setor,
                    aprendiz.observacao,
                    int(aprendiz.ativo),
                    aprendiz.data_atualizacao,
                    aprendiz.id,
                ),
            )

    def listar(self, termo: str = "") -> list[Aprendiz]:
        termo = termo.strip()
        parametros: tuple[str, ...] = ()
        filtro = ""

        if termo:
            like = f"%{termo}%"
            parametros = (like, like, like)
            filtro = """
                WHERE nome LIKE ?
                   OR cpf LIKE ?
                   OR setor LIKE ?
            """

        with obter_conexao() as conexao:
            linhas = conexao.execute(
                f"""
                SELECT *
                  FROM aprendizes
                {filtro}
                 ORDER BY id DESC
                """,
                parametros,
            ).fetchall()
            return [Aprendiz.from_row(linha) for linha in linhas]

    def obter_por_id(self, aprendiz_id: int) -> Aprendiz | None:
        with obter_conexao() as conexao:
            linha = conexao.execute(
                """
                SELECT *
                  FROM aprendizes
                 WHERE id = ?
                """,
                (aprendiz_id,),
            ).fetchone()
            return Aprendiz.from_row(linha) if linha else None

    def cpf_existe(self, cpf: str, ignorar_id: int | None = None) -> bool:
        parametros: list = [cpf]
        filtro = ""
        if ignorar_id is not None:
            filtro = "AND id <> ?"
            parametros.append(ignorar_id)

        with obter_conexao() as conexao:
            linha = conexao.execute(
                f"""
                SELECT 1
                  FROM aprendizes
                 WHERE cpf = ?
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
                  FROM aprendizes
                 WHERE ativo = 1
                """
            ).fetchone()
            return int(linha["total"])

    def atualizar_ativo(self, aprendiz_id: int, ativo: bool) -> None:
        with obter_conexao() as conexao:
            conexao.execute(
                """
                UPDATE aprendizes
                   SET ativo = ?,
                       data_atualizacao = ?
                 WHERE id = ?
                """,
                (
                    int(ativo),
                    datetime.now().isoformat(timespec="seconds"),
                    aprendiz_id,
                ),
            )
