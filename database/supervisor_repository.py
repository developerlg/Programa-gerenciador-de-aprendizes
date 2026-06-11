from database.conexao import obter_conexao


class SupervisorRepository:
    def listar_ativos(self) -> list[str]:
        with obter_conexao() as conexao:
            linhas = conexao.execute(
                """
                SELECT nome
                  FROM supervisores
                 WHERE ativo = 1
                 ORDER BY nome
                """
            ).fetchall()
            return [str(linha["nome"]) for linha in linhas]
