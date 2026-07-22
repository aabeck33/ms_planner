# Consolidador de Tarefas Excel

Projeto responsável por transformar tarefas e checklists exportados do Microsoft Planner em uma planilha orientada por ações, consolidando um ou mais arquivos Excel em uma única saída.

## Funcionalidades

- Leitura de arquivos Excel exportados do Planner.
- Suporte a um único arquivo ou múltiplos arquivos de entrada.
- Consolidação automática dos dados em uma única planilha.
- Desmembramento dos itens de checklist em ações individuais.
- Identificação automática do responsável de cada ação.
- Cálculo do percentual de execução da tarefa.
- Geração de identificadores únicos para cada ação.
- Inclusão da coluna **Projeto**, obtida a partir do nome do arquivo de origem.
- Geração da aba **Detalhes**.
- Atualização automática da aba **Gantt**.

---

## Requisitos

- Python 3.14+
- pip

---

## Instalação

```bash
python -m venv .venv

# Linux / Mac
source .venv/bin/activate

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

---

## Configuração

Crie um arquivo `.env` na raiz do projeto.

### Utilizando um único arquivo de entrada

```env
INPUT_FILE=Projeto_A.xlsx
OUTPUT_FILE=acoes_consolidadas.xlsx
```

### Utilizando múltiplos arquivos de entrada

```env
INPUT_FILE=Projeto_A.xlsx,Projeto_B.xlsx,Projeto_C.xlsx
OUTPUT_FILE=acoes_consolidadas.xlsx
```

### Configurações opcionais

```env
SHEET_NAME=Dados Consolidados
OUTPUT_SHEET_NAME=Detalhes
```

---

## Estrutura dos Arquivos

Coloque os arquivos Excel de entrada dentro da pasta:

```text
work/
```

Exemplo:

```text
work/
├── Projeto_A.xlsx
├── Projeto_B.xlsx
└── Projeto_C.xlsx
```

---

## Execução

```bash
python src/main.py
```

---

## Resultado

Será gerado:

```text
work/acoes_consolidadas.xlsx
```

O arquivo conterá:

- Aba **Detalhes**
- Aba **Gantt**

---

## Coluna Projeto

Ao processar múltiplos arquivos, o sistema cria a coluna **Projeto** automaticamente.

O valor dessa coluna corresponde ao nome do arquivo sem a extensão.

### Exemplo

Arquivo:

```text
Projeto_Migracao.xlsx
```

Valor gerado:

```text
Projeto_Migracao
```

### Exemplo de saída

| Projeto | Identificador | Categoria | Tarefa | Ação |
|----------|---------------|-----------|---------|------|
| Projeto_A | C01.T001.A001 | Planejamento | Definir escopo | Reunião inicial |
| Projeto_A | C01.T001.A002 | Planejamento | Definir escopo | Aprovação |
| Projeto_B | C01.T001.A001 | Execução | Implantação | Configuração |

---

## Identificador das Ações

Formato:

```text
C01.T001.A001
```

Onde:

```text
C01 = Categoria
T001 = Tarefa
A001 = Ação
```

Exemplo:

```text
C03.T015.A004
```

- Categoria 03
- Tarefa 015
- Ação 004

---

## Cálculo do Percentual de Execução

Exemplo:

```text
Itens concluídos da lista de verificação = 3/5
```

Cálculo:

```text
(3 × 100) ÷ 5 = 60%
```

O resultado é gravado na coluna:

```text
Porcentagem de execução da tarefa
```

---

## Tratamento de Responsáveis

Quando uma ação possui um responsável indicado no checklist utilizando o formato:

```text
@Joao Validar documento
```

O sistema:

- identifica o responsável (`Joao`);
- remove a marcação da descrição da ação;
- grava o responsável na coluna correspondente.

Caso não exista responsável definido na ação, será utilizado o valor da coluna **Atribuído a** da tarefa.

---

## Logs

Durante a execução são exibidas informações sobre:

- arquivos processados;
- quantidade de ações geradas;
- geração da aba Detalhes;
- atualização da aba Gantt;
- erros e avisos de processamento.

---