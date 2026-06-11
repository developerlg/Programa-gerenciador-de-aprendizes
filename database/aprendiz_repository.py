from datetime import datetime

from database.conexao import obter_conexao
from models.aprendiz import Aprendiz


class AprendizRepository:
    def criar(self, aprendiz: Aprendiz) -> int:
        with obter_conexao() as conexao:
            cursor = conexao.execute(
                """
                INSERT INTO aprendizes (
                    nome_completo,
                    supervisor_responsavel,
                    data_nascimento,
                    data_admissao,
                    setor,
                    observacoes,
                    status,
                    data_cadastro,
                    data_atualizacao
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    aprendiz.nome_completo,
                    aprendiz.supervisor_responsavel,
                    aprendiz.data_nascimento,
                    aprendiz.data_admissao,
                    aprendiz.setor,
                    aprendiz.observacoes,
                    aprendiz.status,
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
                   SET nome_completo = ?,
                       supervisor_responsavel = ?,
                       data_nascimento = ?,
                       data_admissao = ?,
                       setor = ?,
                       observacoes = ?,
                       status = ?,
                       data_atualizacao = ?
                 WHERE id = ?
                """,
                (
                    aprendiz.nome_completo,
                    aprendiz.supervisor_responsavel,
                    aprendiz.data_nascimento,
                    aprendiz.data_admissao,
                    aprendiz.setor,
                    aprendiz.observacoes,
                    aprendiz.status,
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
            parametros = (like, like, like, like)
            filtro = """
                WHERE nome_completo LIKE ?
                   OR supervisor_responsavel LIKE ?
                   OR setor LIKE ?
                   OR status LIKE ?
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

    def atualizar_status(self, aprendiz_id: int, status: str) -> None:
        with obter_conexao() as conexao:
            conexao.execute(
                """
                UPDATE aprendizes
                   SET status = ?,
                       data_atualizacao = ?
                 WHERE id = ?
                """,
                (
                    status,
                    datetime.now().isoformat(timespec="seconds"),
                    aprendiz_id,
                ),
            )
