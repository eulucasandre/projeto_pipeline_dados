# Pipeline ETL — Fusão de Dados de Mercado

> Projeto de Engenharia de Dados que demonstra, de ponta a ponta, um pipeline ETL (Extract, Transform, Load) para consolidar registros de vendas de duas empresas com estruturas de dados distintas.

---

## Contexto

Imagine que duas empresas do mesmo grupo foram adquiridas e agora precisam ter seus dados de vendas unificados em um único arquivo para análises conjuntas. O problema: cada empresa armazenou suas informações em formatos e com nomes de colunas completamente diferentes — uma usa JSON, a outra usa CSV, e os cabeçalhos não batem.

Este projeto resolve exatamente isso, construindo um pipeline automatizado que lê, padroniza e combina os dados sem nenhuma intervenção manual.

---

## O que você vai encontrar aqui

```
├── data_raw/
│   ├── dados_empresaA.json        # Fonte original — Empresa A (3.123 registros)
│   └── dados_empresaB.csv         # Fonte original — Empresa B (1.323 registros)
│
├── data_processed/
│   └── dados_combinados.csv       # Dataset unificado (4.446 registros)
│
├── explore.ipynb                  # Notebook de exploração e prototipagem
├── processamento_dados.py         # Classe Dados (versão base)
├── fusao_mercado_fev.py           # Pipeline ETL (versão base)
├── processamento_dados_desafio.py # Classe Dados (versão com boas práticas OOP)
└── fusao_mercado_fev_desafio.py   # Pipeline ETL (versão desafio)
```

---

## As três etapas do ETL

### 1. Extract — Extração

Os dados brutos vêm de duas fontes com formatos diferentes:

| Empresa | Formato | Registros | Colunas originais |
|---------|---------|-----------|-------------------|
| Empresa A | `.json` | 3.123 | Nome do Produto, Categoria do Produto, Preço do Produto (R$), Quantidade em Estoque, Filial |
| Empresa B | `.csv`  | 1.323 | Nome do Item, Classificação do Produto, Valor em Reais (R$), Quantidade em Estoque, Nome da Loja, Data da Venda |

A classe `Dados` abstrai a leitura: você passa o caminho e o formato (`'json'` ou `'csv'`), e ela já retorna os registros como uma lista de dicionários padronizada.

### 2. Transform — Transformação

Antes de combinar, é preciso que as colunas falem a mesma língua. Um dicionário de mapeamento renomeia os campos da Empresa B para coincidir com os da Empresa A:

```python
mapeamento_colunas = {
    'Nome do Item'             : 'Nome do Produto',
    'Classificação do Produto' : 'Categoria do Produto',
    'Valor em Reais (R$)'      : 'Preço do Produto (R$)',
    'Quantidade em Estoque'    : 'Quantidade em Estoque',
    'Nome da Loja'             : 'Filial',
    'Data da Venda'            : 'Data da Venda',
}
```

Após a renomeação, os dois datasets têm exatamente as mesmas colunas e podem ser concatenados com segurança.

> **Detalhe importante:** campos ausentes em alguma das fontes não geram erros — o pipeline preenche automaticamente com `'Indisponível'`.

### 3. Load — Carga

O dataset unificado (4.446 registros) é exportado para um único arquivo CSV em `data_processed/dados_combinados.csv`, pronto para ser usado em análises ou carregado em um banco de dados.

---

## Duas versões do código

O projeto tem duas implementações da mesma lógica, com propósitos diferentes:

### Versão base (`processamento_dados.py`)

Abordagem direta e didática. A classe `Dados` recebe o caminho e o formato no construtor e já executa a leitura:

```python
fonte = Dados('data_raw/dados_empresaA.json', 'json')
```

Boa para entender o fluxo sem camadas de abstração adicionais.

### Versão desafio (`processamento_dados_desafio.py`)

Aplica boas práticas de Programação Orientada a Objetos:

- **Métodos privados** com prefixo `__` — protege a implementação interna e deixa a interface pública mais limpa.
- **Factory method** (`leitura_dados`) — separa a responsabilidade de leitura do construtor. O `__init__` só monta o objeto; quem cria a partir de arquivo é o classmethod.

```python
fonte = Dados.leitura_dados('data_raw/dados_empresaA.json', 'json')
```

Esta versão reflete um padrão mais próximo do que você encontraria em projetos profissionais.

---

## Como reproduzir o projeto

**Pré-requisitos:** Python 3.8+

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/pipeline-etl-fusao-mercado.git
cd pipeline-etl-fusao-mercado
```

### 2. Crie e ative o ambiente virtual

O uso de `venv` é uma boa prática mesmo aqui, onde não há dependências externas. Ele isola o projeto do Python global da sua máquina e já deixa o ambiente preparado caso novas bibliotecas sejam adicionadas futuramente.

**Linux / macOS**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows**
```bash
python -m venv .venv
.venv\Scripts\activate
```

Você saberá que o ambiente está ativo quando o nome `.venv` aparecer no início do terminal:
```
(.venv) $
```

Para desativar quando terminar:
```bash
deactivate
```

### 3. Instale as dependências

Este projeto utiliza apenas a biblioteca padrão do Python (`json` e `csv`), então não há pacotes externos para instalar. Ainda assim, o padrão é manter um arquivo `requirements.txt` no repositório — útil para quando o projeto crescer.

```bash
# Nenhuma instalação necessária por enquanto.
# Caso o projeto evolua, as dependências estarão em:
pip install -r requirements.txt
```

### 4. Execute o pipeline

```bash
# Crie a pasta de saída, se ainda não existir
mkdir -p data_processed

# Versão base
python fusao_mercado_fev.py

# Versão com boas práticas OOP
python fusao_mercado_fev_desafio.py
```

Ao final, o arquivo `data_processed/dados_combinados.csv` estará gerado.

---

## Exploração e prototipagem

O notebook `explore.ipynb` documenta o raciocínio por trás do pipeline: como os dados foram inspecionados, por que `csv.DictReader` foi escolhido no lugar de `csv.reader`, e como a lógica de renomeação e combinação foi desenvolvida antes de ser encapsulada na classe. É um bom ponto de partida para entender as decisões de design.

---

## Conceitos demonstrados

- **ETL (Extract, Transform, Load)** — estrutura clássica de pipelines de dados
- **Leitura de múltiplos formatos** — JSON nativo com `json.load` e CSV com `csv.DictReader`
- **Padronização de esquemas** — mapeamento de colunas entre fontes heterogêneas
- **Encapsulamento com OOP** — classe que centraliza leitura, transformação e exportação
- **Métodos privados e factory methods** — boas práticas de design em Python
- **Tratamento de dados ausentes** — valor padrão via `dict.get(chave, 'Indisponível')`

---

## Próximos passos possíveis

Algumas ideias para evoluir o projeto:

- Adicionar suporte a leitura de arquivos `.xlsx` (com `openpyxl` ou `pandas`)
- Implementar validação de schema antes da combinação
- Incluir logs estruturados no pipeline
- Criar testes unitários para a classe `Dados`
- Conectar o Load a um banco de dados (SQLite, PostgreSQL)

---

*Desenvolvido como projeto prático de introdução à Engenharia de Dados.*
