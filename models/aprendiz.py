from dataclasses import dataclass
from typing import Any, Mapping


@dataclass
class Aprendiz:
    nome_completo: str
    supervisor_responsavel: str
    data_cadastro: str
    id: int | None = None
    data_nascimento: str = ""
    data_admissao: str = ""
    setor: str = ""
    observacoes: str = ""
    status: str = "Ativo"
    data_atualizacao: str = ""

    @classmethod
    def from_row(cls, row: Mapping[str, Any]) -> "Aprendiz":
        return cls(
            id=row["id"],
            nome_completo=row["nome_completo"],
            supervisor_responsavel=row["supervisor_responsavel"],
            data_nascimento=row["data_nascimento"] or "",
            data_admissao=row["data_admissao"] or "",
            setor=row["setor"] or "",
            observacoes=row["observacoes"] or "",
            status=row["status"],
            data_cadastro=row["data_cadastro"],
            data_atualizacao=row["data_atualizacao"] or "",
        )
