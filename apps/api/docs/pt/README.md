# Documentação da API ANS Data Processor

## Visão Geral

A API ANS Data Processor é uma ferramenta projetada para processar e analisar dados de saúde da Agência Nacional de Saúde Suplementar (ANS). Ela oferece endpoints para gerenciar dados contábeis, informações de operadoras, processamento de PDFs, extração de CSV e análises.

## Endpoints da API

### 1. Endpoints Contábeis

#### GET /accounting

- **Descrição**: Recuperar uma lista paginada de lançamentos contábeis
- **Parâmetros**:
  - `limit` (int): Número de itens a retornar (padrão: 50, mínimo: 1, máximo: 1000)
  - `cursor` (str): Cursor para paginação
- **Resposta**:
  ```json
  {
    "data": [
      {
        "data": "YYYY-MM-DD",
        "reg_ans": int,
        "cd_conta_contabil": int,
        "descricao": string,
        "vl_saldo_inicial": float,
        "vl_saldo_final": float
      }
    ],
    "next_cursor": string
  }
  ```

#### GET /accounting/{reg_ans}

- **Descrição**: Recuperar lançamentos contábeis para uma operadora específica
- **Parâmetros**:
  - `reg_ans` (int): Número de registro da operadora
- **Resposta**:
  ```json
  [
    {
      "data": "YYYY-MM-DD",
      "reg_ans": int,
      "cd_conta_contabil": int,
      "descricao": string,
      "vl_saldo_inicial": float,
      "vl_saldo_final": float
    }
  ]
  ```

#### POST /accounting/import

- **Descrição**: Importar dados contábeis de um arquivo CSV
- **Corpo da Requisição**:
  - `file` (UploadFile): Arquivo CSV contendo dados contábeis

### 2. Endpoints de Operadoras

#### GET /operators

- **Descrição**: Recuperar uma lista paginada de operadoras de saúde
- **Parâmetros**:
  - `limit` (int): Número de itens a retornar (padrão: 50, mínimo: 1, máximo: 1000)
  - `cursor` (str): Cursor para paginação
- **Resposta**:
  ```json
  {
    "data": [
        {
            "registro_ans": int,
            "cnpj": string,
            "razao_social": string,
            "nome_fantasia": string,
            "modalidade": string,
            "logradouro": string,
            "numero": int,
            "complemento": string,
            "bairro": string,
            "cidade": string,
            "uf": string,
            "cep": int,
            "ddd": int,
            "telefone": int,
            "fax": int,
            "endereco_eletronico": string,
            "representante": string,
            "cargo_representante": string,
            "regiao_de_comercializacao": int,
            "data_registro_ans": "YYYY-MM-DD"
        }
    ],
    "next_cursor": string
  }
  ```

#### GET /operators/id/{registro_ans}

- **Descrição**: Recuperar informações sobre uma operadora específica
- **Parâmetros**:
  - `registro_ans` (int): Número de registro da operadora
- **Resposta**:
  ```json
  {
    "registro_ans": integer,
    "razao_social": string,
    "cnpj": string,
    "data_registro_ans": "YYYY-MM-DD"
  }
  ```

#### GET /operators/search

- **Descrição**: Busca operadoras por razão social ou nome fantasia usando Levenshtein
- **Parâmetros**:
  - `name` (str): Razão social ou nome fantasia da operadora
  - `city` (str): Cidade da operadora
  - `state` (str): Estado da operadora
  - `modality` (str): Modalidade da operadora
- **Resposta**:
  ```json
  {
    "items": [
        {
          "registro_ans": integer,
          "razao_social": string,
          "cnpj": string,
          "data_registro_ans": "YYYY-MM-DD"
        }
    ]
  }
  ```

#### POST /operators/import

- **Descrição**: Importar dados de operadoras de um arquivo CSV
- **Corpo da Requisição**:
  - `file` (UploadFile): Arquivo CSV contendo dados das operadoras

### 3. Endpoints de Processamento de PDF

#### GET /pdf/ans

- **Descrição**: Processar arquivos PDF da ANS
- **Parâmetros**:
  - `target_url` (str): URL da ANS
- **Resposta**:
  ```json
  {
    "url": "https://r2.example.com/pdfs/processed/file.zip"
  }
  ```

#### GET /pdf/scrap

- **Descrição**: Processar e embutir arquivos PDF da ANS
- **Parâmetros**:
  - `target_url` (str): URL de destino
  - `target_file` (str): Nome do arquivo de destino
- **Resposta**:
  ```json
  {
    "url": "https://r2.example.com/pdfs/processed/file.pdf"
  }
  ```

### 4. Endpoints de Processamento de CSV

#### GET /csv/extract-tables

- **Descrição**: Extrair tabelas de um arquivo PDF
- **Parâmetros**:
  - `target_file` (str): Nome do arquivo de destino
- **Resposta**:
  ```json
  {
    "url": "https://r2.example.com/tables.zip"
  }
  ```

#### GET /csv/download-table

- **Descrição**: Extrair tabelas de um PDF e baixar o arquivo processado
- **Resposta**:
  ```json
  {
    "url": "https://r2.example.com/processed/file.csv"
  }
  ```

### 5. Endpoints de Análise

#### GET /analytics/expenses/quarterly

- **Descrição**: Obter as principais despesas do trimestre atual
- **Resposta**:
  ```json
  [
    {
      "operator": string,
      "registro_ans": integer,
      "total_expenses": float
    }
  ]
  ```

#### GET /analytics/expenses/yearly

- **Descrição**: Obter as principais despesas do ano atual
- **Resposta**:
  ```json
  [
    {
      "operator": string,
      "registro_ans": integer,
      "total_expenses": float
    }
  ]
  ```
