# ANS Data Processor API Documentation

## Overview

The ANS Data Processor API is a tool designed to process and analyze healthcare data from the Brazilian National Health Agency (ANS). It provides endpoints for managing accounting data, operator information, PDF processing, CSV extraction, and analytics.

## API Endpoints

### 1. Accounting Endpoints

#### GET /accounting

- **Description**: Retrieve a paginated list of accounting entries
- **Parameters**:
  - `limit` (int): Number of items to return (default: 50, min: 1, max: 1000)
  - `cursor` (str): Cursor for pagination
- **Response**:
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

- **Description**: Retrieve accounting entries for a specific operator
- **Parameters**:
  - `reg_ans` (int): Operator registration number
- **Response**:
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

- **Description**: Import accounting data from a CSV file
- **Request Body**:
  - `file` (UploadFile): CSV file containing accounting data

### 2. Operator Endpoints

#### GET /operators

- **Description**: Retrieve a paginated list of healthcare operators
- **Parameters**:
  - `limit` (int): Number of items to return (default: 50, min: 1, max: 1000)
  - `cursor` (str): Cursor for pagination
- **Response**:
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

- **Description**: Retrieve information about a specific operator
- **Parameters**:
  - `registro_ans` (int): Operator registration number
- **Response**:

```json
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
```

#### POST /operators/import

- **Description**: Import operator data from a CSV file
- **Request Body**:
  - `file` (UploadFile): CSV file containing operator data

#### GET /operators/search

- **Description**: Search operators by corporate name or trade name using Levenshtein distance
- **Parameters**:
  - `name` (str): Corporate name or trade name of the operator
  - `city` (str): City of the operator
  - `state` (str): State of the operator
  - `modality` (str): Modality of the operator
- **Response**:
  ```json
  {
    "registro_ans": integer,
    "razao_social": string,
    "cnpj": string,
    "data_registro_ans": "YYYY-MM-DD"
  }
  ```

### 3. PDF Processing Endpoints

#### GET /pdf/ans

- **Description**: Process ANS PDF files
- **Parameters**:
  - `target_url` (str): ANS URL
- **Response**:
  ```json
  {
    "url": "https://r2.example.com/pdfs/processed/file.zip"
  }
  ```

#### GET /pdf/scrap

- **Description**: Process and embed ANS PDF files
- **Parameters**:
  - `target_url` (str): Target URL
  - `target_file` (str): Target file name
- **Response**:
  ```json
  {
    "url": "https://r2.example.com/pdfs/processed/file.pdf"
  }
  ```

### 4. CSV Processing Endpoints

#### GET /csv/extract-tables

- **Description**: Extract tables from a PDF file
- **Parameters**:
  - `target_file` (str): Target file name
- **Response**:
  ```json
  {
    "url": "https://r2.example.com/tables.zip"
  }
  ```

#### GET /csv/download-table

- **Description**: Extract tables from a PDF and download the processed file
- **Response**:
  ```json
  {
    "url": "https://r2.example.com/processed/file.csv"
  }
  ```

### 5. Analytics Endpoints

#### GET /analytics/expenses/quarterly

- **Description**: Get top expenses for the current quarter
- **Response**:
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

- **Description**: Get top expenses for the current year
- **Response**:
  ```json
  [
    {
      "operator": string,
      "registro_ans": integer,
      "total_expenses": float
    }
  ]
  ```

```

```
