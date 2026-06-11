from copy import deepcopy

from data.dashboard_mock import DASHBOARD_DATA


class DashboardController:
    def obter_resumo(self) -> dict:
        return deepcopy(DASHBOARD_DATA)
