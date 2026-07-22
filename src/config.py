import os
import logging
from typing import Final
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


CATEGORY_ORDER: Final[list[str]] = [
    "Inicialização",
    "Planejamento",
    "Execução",
    "Monitoramento e controle",
    "Fechamento",
    "Atividades para Planejar",
    "Atividades para Iniciar",
    "Atividades em Andamento",
]


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s "
            "[%(levelname)s] "
            "%(name)s - %(message)s"
        ),
    )


@dataclass(frozen=True)
class Config:
    work_dir: Path
    input_files: list[Path]
    output_file: Path
    sheet_name: str
    output_sheet_name: str


@dataclass(slots=True)
class ActionRecord:
    identificador: str
    categoria: str
    tarefa: str
    acao: str
    responsavel: str
    status: str
    prioridade: str
    data_inicio: datetime | None
    data_conclusao: datetime | None
    atrasados: str
    concluido_em: datetime | None
    itens_concluidos: str
    percentual_execucao: float


def load_config() -> Config:
    work_dir = Path("work")

    input_name = os.getenv("INPUT_FILE")
    output_name = os.getenv(
        "OUTPUT_FILE",
        "acoes_consolidadas.xlsx",
    )
    sheet_name = os.getenv(
        "SHEET_NAME",
        "Dados Consolidados",
    )
    output_sheet_name = os.getenv(
        "OUTPUT_SHEET_NAME",
        "Detalhes"
    )

    if not input_name:
        raise ValueError(
            "Variável INPUT_FILE não configurada."
        )

    input_files = [
        work_dir / arquivo.strip()
        for arquivo in input_name.split(";")
        if arquivo.strip()
    ]

    return Config(
        work_dir=work_dir,
        input_files=input_files,
        output_file=work_dir / output_name,
        sheet_name=sheet_name,
        output_sheet_name=output_sheet_name,
    )
