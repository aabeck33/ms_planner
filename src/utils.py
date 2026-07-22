import re
from datetime import datetime, date
from typing import Optional
import logging
import pandas as pd
from config import load_config

logger = logging.getLogger(__name__)
config = load_config()

def extract_responsavel(action: str) -> str:
    match = re.search(r"@([^\s;]+)", action)

    if match:
        return match.group(1)

    return ""


def calcular_percentual(valor: str) -> float:
    """
    Exemplo:
    3/5 -> (3 * 100) / 5 = 60
    """

    if not valor:
        return 0.0

    try:
        concluido, total = valor.split("/")

        concluido_num = float(concluido.strip())
        total_num = float(total.strip())

        if total_num == 0:
            return 0.0

        return round(
            (concluido_num * 100) / total_num,
            2,
        )

    except Exception:
        return 0.0


def criar_identificador(
    categoria_idx: int,
    tarefa_idx: int,
    acao_idx: int,
) -> str:
    return (
        f"C{categoria_idx:02d}"
        f".T{tarefa_idx:03d}"
        f".A{acao_idx:03d}"
    )



def limpar_acao(acao: str) -> str:
    return re.sub(
        r"@\S+\s*",
        "",
        acao,
        count=1
    ).strip()


def carregar_planilha(
    arquivo: str,
) -> pd.DataFrame:
    logger.info(
        "Lendo aba '%s' do arquivo %s",
        config.sheet_name,
        arquivo,
    )

    return pd.read_excel(
        arquivo,
        config.sheet_name,
        engine="openpyxl",
    )


def converter_data(valor) -> date | None:

    if not valor:
        return None

    if isinstance(valor, date):
        return valor

    try:
        return datetime.strptime(
            str(valor),
            "%Y-%m-%d"
        ).date()

    except Exception:
        return None
