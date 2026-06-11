from datetime import date, datetime

from database.aprendiz_repository import AprendizRepository
from database.supervisor_repository import SupervisorRepository
from models.aprendiz import Aprendiz


class ValidationError(ValueError):
    pass


class AprendizService:
    def __init__(
        self,
        aprendiz_repository: AprendizRepository | None = None,
        supervisor_repository: SupervisorRepository | None = None,
    ):
        self.aprendiz_repository = aprendiz_repository or AprendizRepository()
        self.supervisor_repository = supervisor_repository or SupervisorRepository()

    def criar(self, dados: dict) -> int:
        aprendiz = self._montar_aprendiz(dados, data_cadastro=date.today().isoformat())
        self._validar_cpf_unico(aprendiz.cpf)
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
        self._validar_cpf_unico(aprendiz.cpf, ignorar_id=aprendiz_id)
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
        self.aprendiz_repository.atualizar_ativo(aprendiz_id, False)

    def listar_supervisores_ativos(self) -> list[dict]:
        supervisores = self.supervisor_repository.listar_ativos()
        return [
            {
                "id": supervisor.id,
                "nome": supervisor.nome,
                "funcao": supervisor.funcao,
            }
            for supervisor in supervisores
        ]

    def _montar_aprendiz(
        self,
        dados: dict,
        data_cadastro: str,
        aprendiz_id: int | None = None,
    ) -> Aprendiz:
        nome = self._texto_obrigatorio(dados.get("nome"), "Nome")
        cpf = self._normalizar_cpf(dados.get("cpf"))
        supervisor_id = self._inteiro_obrigatorio(dados.get("supervisor_id"), "Supervisor")
        supervisor = self.supervisor_repository.obter_por_id(supervisor_id)

        if not supervisor or not supervisor.ativo:
            raise ValidationError("Selecione um supervisor ativo.")

        return Aprendiz(
            id=aprendiz_id,
            nome=nome,
            cpf=cpf,
            setor=self._texto_obrigatorio(dados.get("setor"), "Setor"),
            observacao=self._texto_opcional(dados.get("observacao")),
            supervisor_id=supervisor_id,
            ativo=bool(dados.get("ativo", True)),
            data_cadastro=data_cadastro,
            data_atualizacao=datetime.now().isoformat(timespec="seconds"),
        )

    def _para_view_model(self, aprendiz: Aprendiz) -> dict:
        return {
            "id": aprendiz.id,
            "nome": aprendiz.nome,
            "cpf": self._formatar_cpf(aprendiz.cpf),
            "cpf_raw": aprendiz.cpf,
            "setor": aprendiz.setor,
            "observacao": aprendiz.observacao,
            "supervisor_id": aprendiz.supervisor_id,
            "supervisor_nome": aprendiz.supervisor_nome,
            "status": "Ativo" if aprendiz.ativo else "Inativo",
            "ativo": aprendiz.ativo,
            "data_cadastro": self._formatar_data(aprendiz.data_cadastro),
        }

    def _validar_cpf_unico(self, cpf: str, ignorar_id: int | None = None) -> None:
        if self.aprendiz_repository.cpf_existe(cpf, ignorar_id):
            raise ValidationError("Ja existe aprendiz cadastrado com este CPF.")

    def _texto_obrigatorio(self, valor, campo: str) -> str:
        texto = str(valor or "").strip()
        if not texto:
            raise ValidationError(f"{campo} e obrigatorio.")
        return texto

    def _texto_opcional(self, valor) -> str:
        return str(valor or "").strip()

    def _inteiro_obrigatorio(self, valor, campo: str) -> int:
        try:
            inteiro = int(valor)
        except (TypeError, ValueError):
            raise ValidationError(f"{campo} e obrigatorio.") from None

        if inteiro <= 0:
            raise ValidationError(f"{campo} e obrigatorio.")
        return inteiro

    def _normalizar_cpf(self, valor) -> str:
        cpf = "".join(ch for ch in str(valor or "") if ch.isdigit())
        if len(cpf) != 11:
            raise ValidationError("CPF deve conter 11 digitos.")
        return cpf

    def _formatar_cpf(self, cpf: str) -> str:
        if len(cpf) != 11:
            return cpf
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

    def _formatar_data(self, valor: str) -> str:
        if not valor:
            return ""

        for formato in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S"):
            try:
                return datetime.strptime(valor, formato).strftime("%d/%m/%Y")
            except ValueError:
                continue

        return valor
