from database.dashboard_repository import DashboardRepository


class DashboardController:
    def __init__(self, repository: DashboardRepository | None = None):
        self.repository = repository or DashboardRepository()

    def obter_resumo(self) -> dict:
        resumo = self.repository.obter_resumo()
        return {
            "cards": [
                {
                    "title": "Jovens Aprendizes",
                    "value": str(resumo["aprendizes_ativos"]),
                    "subtitle": "Ativos",
                    "color": "#0B5AC9",
                },
                {
                    "title": "Supervisores",
                    "value": str(resumo["supervisores_ativos"]),
                    "subtitle": "Ativos",
                    "color": "#1FB554",
                },
                {
                    "title": "Atividades",
                    "value": str(resumo["atividades_registradas"]),
                    "subtitle": "Registradas",
                    "color": "#8B95A7",
                },
                {
                    "title": "Prazos",
                    "value": str(resumo["prazos_registrados"]),
                    "subtitle": "Cadastrados",
                    "color": "#8B95A7",
                },
            ],
            "recent_activities": [],
            "status_chart": [
                ("Em andamento", 0, "#2F80ED"),
                ("Concluídas", 0, "#27AE60"),
                ("Atrasadas", 0, "#EB5757"),
            ],
            "service_chart": [],
            "pending": [
                ("Atividades atrasadas", "0", "#8B95A7"),
                ("Prazos cadastrados", str(resumo["prazos_registrados"]), "#8B95A7"),
            ],
            "deadlines": [],
        }
