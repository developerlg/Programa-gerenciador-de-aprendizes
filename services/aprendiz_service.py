from datetime import date, datetime

from database.aprendiz_repository import AprendizRepository
from models.aprendiz import Aprendiz


class ValidationError(ValueError):
    pass


class AprendizService:
    def __init__(self, aprendiz_repository: AprendizRepository | None = None):
        self.aprendiz_repository = aprendiz_repository or AprendizRepository()

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

    def _montar_aprendiz(
        self,
        dados: dict,
        data_cadastro: str,
        aprendiz_id: int | None = None,
    ) -> Aprendiz:
        return Aprendiz(
            id=aprendiz_id,
            nome=self._texto_obrigatorio(dados.get("nome"), "Nome"),
            cpf=self._normalizar_cpf(dados.get("cpf")),
            setor=self._texto_obrigatorio(dados.get("setor"), "Setor"),
            observacao=self._texto_opcional(dados.get("observacao")),
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
