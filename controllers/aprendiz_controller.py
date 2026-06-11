from services.aprendiz_service import AprendizService


class AprendizController:
    def __init__(self, service: AprendizService | None = None):
        self.service = service or AprendizService()

    def listar_aprendizes(self, termo: str = "") -> list[dict]:
        return self.service.listar(termo)

    def obter_aprendiz(self, aprendiz_id: int) -> dict | None:
        return self.service.obter(aprendiz_id)

    def salvar_aprendiz(self, dados: dict, aprendiz_id: int | None = None) -> None:
        if aprendiz_id:
            self.service.atualizar(aprendiz_id, dados)
            return
        self.service.criar(dados)

    def inativar_aprendiz(self, aprendiz_id: int) -> None:
        self.service.inativar(aprendiz_id)

    def listar_supervisores(self) -> list[str]:
        return self.service.listar_supervisores()
