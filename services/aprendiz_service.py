from datetime import date, datetime

from database.aprendiz_repository import AprendizRepository
from database.supervisor_repository import SupervisorRepository
from models.aprendiz import Aprendiz


class ValidationError(ValueError):
    pass


class AprendizService:
    STATUS_VALIDOS = {"Ativo", "Inativo"}

    def __init__(
        self,
        aprendiz_repository: AprendizRepository | None = None,
        supervisor_repository: SupervisorRepository | None = None,
    ):
        self.aprendiz_repository = aprendiz_repository or AprendizRepository()
        self.supervisor_repository = supervisor_repository or SupervisorRepository()

    def criar(self, dados: dict) -> int:
        aprendiz = self._montar_aprendiz(dados, data_cadastro=date.today().isoformat())
        return self.aprendiz_repository.criar(aprendiz)

    def atualizar(self, aprendiz_id: int, dados: dict) -> None:
        existente = self.aprendiz_repository.obter_por_id(aprendiz_id)
        if not existente:
            raise ValidationError("Aprendiz nao encontrado.")

        aprendiz = self._montar_aprendiz(
            dados,
            aprendiz_id=aprendiz_id,
            data_cadastro=existente.data_cadastro,
        )
        self.aprendiz_repository.atualizar(aprendiz)

    def listar(self, termo: str = "") -> list[dict]:
        aprendizes = self.aprendiz_repository.listar(termo)
        return [self._para_view_model(aprendiz) for aprendiz in aprendizes]

    def obter(self, aprendiz_id: int) -> dict | None:
        aprendiz = self.aprendiz_repository.obter_por_id(aprendiz_id)
        return self._para_view_model(aprendiz) if aprendiz else None

    def inativar(self, aprendiz_id: int) -> None:
        if not self.aprendiz_repository.obter_por_id(aprendiz_id):
            raise ValidationError("Aprendiz nao encontrado.")
        self.aprendiz_repository.atualizar_status(aprendiz_id, "Inativo")

    def listar_supervisores(self) -> list[str]:
        return self.supervisor_repository.listar_ativos()

    def _montar_aprendiz(
        self,
        dados: dict,
        data_cadastro: str,
        aprendiz_id: int | None = None,
    ) -> Aprendiz:
        nome = self._texto_obrigatorio(dados.get("nome_completo"), "Nome completo")
        supervisor = self._texto_obrigatorio(
            dados.get("supervisor_responsavel"),
            "Supervisor responsavel",
        )
        status = (dados.get("status") or "Ativo").strip()

        if status not in self.STATUS_VALIDOS:
            raise ValidationError("Status invalido.")

        return Aprendiz(
            id=aprendiz_id,
            nome_completo=nome,
            supervisor_responsavel=supervisor,
            data_nascimento=self._normalizar_data(dados.get("data_nascimento")),
            data_admissao=self._normalizar_data(dados.get("data_admissao")),
            setor=self._texto_opcional(dados.get("setor")),
            observacoes=self._texto_opcional(dados.get("observacoes")),
            status=status,
            data_cadastro=data_cadastro,
            data_atualizacao=datetime.now().isoformat(timespec="seconds"),
        )

    def _para_view_model(self, aprendiz: Aprendiz) -> dict:
        return {
            "id": aprendiz.id,
            "nome_completo": aprendiz.nome_completo,
            "supervisor_responsavel": aprendiz.supervisor_responsavel,
            "data_nascimento": self._formatar_data(aprendiz.data_nascimento),
            "data_admissao": self._formatar_data(aprendiz.data_admissao),
            "setor": aprendiz.setor,
            "observacoes": aprendiz.observacoes,
            "status": aprendiz.status,
            "data_cadastro": self._formatar_data(aprendiz.data_cadastro),
        }

    def _texto_obrigatorio(self, valor, campo: str) -> str:
        texto = str(valor or "").strip()
        if not texto:
            raise ValidationError(f"{campo} e obrigatorio.")
        return texto

    def _texto_opcional(self, valor) -> str:
        return str(valor or "").strip()

    def _normalizar_data(self, valor) -> str:
        texto = str(valor or "").strip()
        if not texto:
            return ""

        for formato in ("%d/%m/%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(texto, formato).date().isoformat()
            except ValueError:
                continue

        raise ValidationError("Use datas no formato dd/mm/aaaa.")

    def _formatar_data(self, valor: str) -> str:
        if not valor:
            return ""

        for formato in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S"):
            try:
                return datetime.strptime(valor, formato).strftime("%d/%m/%Y")
            except ValueError:
                continue

        return valor
