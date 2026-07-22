'''
        Programa para desmembrar as ações do Planner

        by Alvaro Adriano Beck
        07/2026
'''
import logging
import pandas as pd
from config import load_config
from config import configure_logging
from utils import carregar_planilha
from processor import processar_dados
from processor_gantt import criar_aba_gantt

logger = logging.getLogger(__name__)



def atualizar_gantt(config) -> None:
    logger.info(
        "Gerando arquivo de saída - aba Gantt..."
    )

    criar_aba_gantt(
        str(config.output_file),
        config.output_sheet_name,
    )

    logger.info(
        "Aba Gantt atualizada."
    )



def main() -> None:
    configure_logging()
    config = load_config()

    logger.info(
        "Arquivos de entrada: %s",
        config.input_files,
    )

    if not any(
        arquivo.exists()
        for arquivo in config.input_files
    ):
        '''raise FileNotFoundError(
            f"Arquivo não encontrado: "
            f"{config.input_file}"
        )'''
        
        logger.warning(
            "Arquivo de entrada não encontrado: %s",
            config.input_file,
        )

        resposta = input(
            "\nArquivo de entrada não encontrado.\n"
            "Deseja recriar apenas a aba Gantt "
            "utilizando o arquivo de saída existente? (S/N): "
        ).strip().upper()

        if resposta != "S":
            logger.info(
                "Processamento cancelado pelo usuário."
            )
            return

        if not config.output_file.exists():
            logger.error(
                "Arquivo de saída '%s' não encontrado.",
                config.output_file,
            )
            return

        atualizar_gantt(config)

        logger.info(
            "Arquivo atualizado: %s",
            config.output_file,
        )

        return

    resultados = []

    for arquivo in config.input_files:

        logger.info(
            "Arquivo de entrada: %s",
            arquivo,
        )

        if not arquivo.exists():
            logger.warning(
                "Arquivo não encontrado: %s",
                arquivo,
            )
            continue

        dataframe = carregar_planilha(
            str(arquivo)
        )

        projeto = arquivo.stem

        resultado_parcial = processar_dados(
            dataframe,
            projeto,
        )

        resultados.append(
            resultado_parcial
        )

    if not resultados:
        logger.error(
            "Nenhum arquivo válido encontrado."
        )
        return

    resultado = pd.concat(
        resultados,
        ignore_index=True,
    )

    try:
        logger.info(
            "Gerando arquivo de saída - aba %s...",
            config.output_sheet_name
        )

        resultado.to_excel(
            config.output_file,
            sheet_name=config.output_sheet_name,
            index=False,
            engine="openpyxl",
        )
    
    except PermissionError:
        logger.error(
            "Arquivo '%s' está aberto ou bloqueado. "
            "Feche o Excel e tente novamente.",
            config.output_file,
        )
        return

    atualizar_gantt(config)

    logger.info(
        "Arquivo gerado: %s",
        config.output_file,
    )


if __name__ == "__main__":
    main()
