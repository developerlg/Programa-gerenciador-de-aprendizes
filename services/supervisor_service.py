from datetime import datetime

from database.supervisor_repository import SupervisorRepository
from models.supervisor import Supervisor
from services.aprendiz_service import ValidationError


class SupervisorService:
    def __init__(self, repository: SupervisorRepository | None = None):
        self.repository = repository or SupervisorRepository()

    def criar(self, dados: dict) -> int:
        supervisor = self._montar_supervisor(dados)
        self._validar_nome_unico(supervisor.nome)
        return self.repository.criar(supervisor)

    def atualizar(self, supervisor_id: int, dados: dict) -> None:
        if not self.repository.obter_por_id(supervisor_id):
            raise ValidationError("Supervisor não encontrado.")

        supervisor = self._montar_supervisor(dados, supervisor_id)
        self._validar_nome_unico(supervisor.nome, supervisor_id)
        self.repository.atualizar(supervisor)

    def listar(self, termo: str = "") -> list[dict]:
        return [self._para_view_model(supervisor) for supervisor in self.repository.listar(termo)]

    def obter(self, supervisor_id: int) -> dict | None:
        supervisor = self.repository.obter_por_id(supervisor_id)
        return self._para_view_model(supervisor) if supervisor else None

    def inativar(self, supervisor_id: int) -> None:
        if not self.repository.obter_por_id(supervisor_id):
            raise ValidationError("Supervisor não encontrado.")
        self.repository.atualizar_ativo(supervisor_id, False)

    def _montar_supervisor(self, dados: dict, supervisor_id: int | None = None) -> Supervisor:
        return Supervisor(
            id=supervisor_id,
            nome=self._texto_obrigatorio(dados.get("nome"), "Nome"),
            funcao=self._texto_obrigatorio(dados.get("funcao"), "Função"),
            setor=self._texto_obrigatorio(dados.get("setor"), "Setor"),
            ativo=bool(dados.get("ativo", True)),
            data_atualizacao=datetime.now().isoformat(timespec="seconds"),
        )

    def _para_view_model(self, supervisor: Supervisor) -> dict:
        return {
            "id": supervisor.id,
            "nome": supervisor.nome,
            "funcao": supervisor.funcao,
            "setor": supervisor.setor,
            "status": "Ativo" if supervisor.ativo else "Inativo",
            "ativo": supervisor.ativo,
        }

    def _validar_nome_unico(self, nome: str, ignorar_id: int | None = None) -> None:
        if self.repository.nome_existe(nome, ignorar_id):
            raise ValidationError("Já existe supervisor cadastrado com este nome.")

    def _texto_obrigatorio(self, valor, campo: str) -> str:
        texto = str(valor or "").strip()
        if not texto:
            raise ValidationError(f"{campo} é obrigatório.")
        return texto
