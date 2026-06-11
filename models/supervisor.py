from dataclasses import dataclass
from typing import Any, Mapping


@dataclass
class Supervisor:
    nome: str
    funcao: str
    id: int | None = None
    ativo: bool = True
    criado_em: str = ""
    data_atualizacao: str = ""

    @classmethod
    def from_row(cls, row: Mapping[str, Any]) -> "Supervisor":
        return cls(
            id=row["id"],
            nome=row["nome"],
            funcao=row["funcao"] or "",
            ativo=bool(row["ativo"]),
            criado_em=row["criado_em"],
            data_atualizacao=row["data_atualizacao"] or "",
        )
