# Processador de Dados ANS

Um sistema completo de processamento de dados projetado para lidar e analisar dados da ANS.

## Estrutura do Projeto

O projeto está organizado em dois componentes principais:

1. **Frontend** - Interface do usuário baseada em Vue.js
2. **Backend** - Serviço de API baseado em Python

## Documentação

- [Documentação do Frontend](./apps/frontend/docs/pt/README.md)
- [Documentação do Backend](./apps/api/docs/pt/README.md)

## Configuração

1. Clone o repositório
2. Instale as dependências:
   ```bash
   npm install
   ```
3. Configure as variáveis de ambiente:
   - Copie `.env.example` para `.env`
   - Atualize as variáveis necessárias

4. Inicie o ambiente de desenvolvimento:
   ```bash
   docker-compose up
   ```

## Tecnologias Utilizadas

- Frontend: Vue.js
- Backend: Python
- Containerização: Docker
- Bucket: Cloudflare R2
- Teste de API: Postman