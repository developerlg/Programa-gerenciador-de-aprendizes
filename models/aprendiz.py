from dataclasses import dataclass
from typing import Any, Mapping


@dataclass
class Aprendiz:
    nome: str
    cpf: str
    setor: str
    observacao: str
    data_cadastro: str
    id: int | None = None
    ativo: bool = True
    data_atualizacao: str = ""

    @classmethod
    def from_row(cls, row: Mapping[str, Any]) -> "Aprendiz":
        return cls(
            id=row["id"],
            nome=row["nome"],
            cpf=row["cpf"],
            setor=row["setor"] or "",
            observacao=row["observacao"] or "",
            ativo=bool(row["ativo"]),
            data_cadastro=row["data_cadastro"],
            data_atualizacao=row["data_atualizacao"] or "",
        )
