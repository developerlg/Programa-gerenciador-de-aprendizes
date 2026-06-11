from services.supervisor_service import SupervisorService


class SupervisorController:
    def __init__(self, service: SupervisorService | None = None):
        self.service = service or SupervisorService()

    def listar_supervisores(self, termo: str = "") -> list[dict]:
        return self.service.listar(termo)

    def obter_supervisor(self, supervisor_id: int) -> dict | None:
        return self.service.obter(supervisor_id)

    def salvar_supervisor(self, dados: dict, supervisor_id: int | None = None) -> None:
        if supervisor_id:
            self.service.atualizar(supervisor_id, dados)
            return
        self.service.criar(dados)

    def inativar_supervisor(self, supervisor_id: int) -> None:
        self.service.inativar(supervisor_id)
