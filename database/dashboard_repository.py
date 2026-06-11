from database.conexao import obter_conexao


class DashboardRepository:
    def obter_resumo(self) -> dict:
        with obter_conexao() as conexao:
            aprendizes_ativos = conexao.execute(
                "SELECT COUNT(*) AS total FROM aprendizes WHERE ativo = 1"
            ).fetchone()["total"]
            supervisores_ativos = conexao.execute(
                "SELECT COUNT(*) AS total FROM supervisores WHERE ativo = 1"
            ).fetchone()["total"]
            atividades = conexao.execute(
                "SELECT COUNT(*) AS total FROM atividades"
            ).fetchone()["total"]
            prazos = conexao.execute(
                """
                SELECT COUNT(*) AS total
                  FROM atividades
                 WHERE prazo_estimado IS NOT NULL
                   AND prazo_estimado <> ''
                """
            ).fetchone()["total"]

        return {
            "aprendizes_ativos": int(aprendizes_ativos),
            "supervisores_ativos": int(supervisores_ativos),
            "atividades_registradas": int(atividades),
            "prazos_registrados": int(prazos),
        }
