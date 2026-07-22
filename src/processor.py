import logging
import pandas as pd
from config import CATEGORY_ORDER
from utils import (
    calcular_percentual,
    criar_identificador,
    extract_responsavel,
    limpar_acao,
)

logger = logging.getLogger(__name__)


def processar_dados(
    df: pd.DataFrame,
    projeto: str,
) -> pd.DataFrame:

    registros: list[dict] = []

    categoria_map = {
        categoria: indice + 1
        for indice, categoria
        in enumerate(CATEGORY_ORDER)
    }

    tarefa_contador: dict[str, int] = {}

    logger.info("Processando tarefas...")

    for _, row in df.iterrows():

        categoria = str(
            row.get("Categoria", "")
        ).strip()

        tarefa_contador.setdefault(
            categoria,
            0,
        )

        tarefa_contador[categoria] += 1

        tarefa_idx = tarefa_contador[categoria]

        checklist = str(
            row.get(
                "Itens da lista de verificação",
                "",
            )
        )

        acoes = [
            a.strip()
            for a in checklist.split(";")
            if a.strip()
        ]

        percentual = calcular_percentual(
            str(
                row.get(
                    "Itens concluídos da lista de verificação",
                    ""
                )
            )
        )

        for acao_idx, acao in enumerate(
            acoes,
            start=1,
        ):

            identificador = criar_identificador(
                categoria_map.get(
                    categoria,
                    99,
                ),
                tarefa_idx,
                acao_idx,
            )

            registros.append(
                {
                    "Projeto": projeto,
                    "Identificador": identificador,
                    "Categoria": categoria,
                    "Tarefa": row.get("Nome da tarefa"),
                    "Ação": (
                        limpar_acao(acao)
                    ),
                    "Responsável": (
                        extract_responsavel(acao)
                        or str(row.get("Atribuído a", "")).strip()
                    ),
                    "Status": row.get("Status"),
                    "Prioridade": row.get("Prioridade"),
                    "Data de início": row.get("Data de início"),
                    "Data de conclusão": row.get("Data de conclusão"),
                    "Atrasados": row.get("Atrasados"),
                    "Concluído em": row.get("Concluído em"),
                    "Itens concluídos da lista de verificação":
                        row.get("Itens concluídos da lista de verificação"),
                    "Porcentagem de execução da tarefa": 
                        percentual,
                }
            )

    resultado = pd.DataFrame(
        registros
    )

    '''resultado["ordem_categoria"] = (
        resultado["Categoria"].map(
            {
                cat: idx
                for idx, cat
                in enumerate(
                    CATEGORY_ORDER
                )
            }
        )
    )'''

    resultado.sort_values(
        by=["Identificador"],
        inplace=True,
    )

    resultado.reset_index(
        drop=True,
        inplace=True,
    )

    '''resultado.drop(
        columns=["ordem_categoria"],
        inplace=True,
    )'''

    logger.info(
        "%s ações processadas.",
        len(resultado),
    )

    return resultado
