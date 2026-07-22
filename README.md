# Consolidador de Tarefas Excel

Projeto responsável por transformar tarefas e checklists da aba
"Dados Consolidados" em uma planilha orientada por ações.

## Requisitos

- Python 3.14+
- pip

## Instalação

```bash
python -m venv .venv

# Linux/Mac
source .venv/bin/activate

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

## Configuração

Arquivo `.env`:

```env
INPUT_FILE=entrada.xlsx
OUTPUT_FILE=acoes_consolidadas.xlsx
```

Coloque o arquivo Excel dentro do diretório:

```text
work/
```

## Execução

```bash
python src/main.py
```

## Resultado

Será gerado:

```text
work/acoes_consolidadas.xlsx
```

## Identificador

Formato:

```text
C01.T001.A001
│   │    │
│   │    └── Ação
│   └─────── Tarefa
└─────────── Categoria
```

## Cálculo de percentual

Exemplo:

```text
Itens concluídos da lista de verificação = 3/5

(3 × 100) ÷ 5 = 60%
```
