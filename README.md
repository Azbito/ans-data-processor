# ANS Data Processor

A comprehensive data processing system designed to handle and analyze ANS data.

## Project Structure

The project is organized into two main components:

1. **Frontend** - Vue.js based user interface
2. **Backend** - Python-based API service

## Documentation

- [Frontend Documentation](./apps/frontend/docs/en/README.md)
- [Backend Documentation](./apps/api/docs/en/README.md)

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   npm install
   ```
3. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Update the necessary variables

4. Start the development environment:
   ```bash
   docker-compose up
   ```

## Technologies Used

- Frontend: Vue.js
- Backend: Python
- Containerization: Docker
- Bucket: Cloudflare R2
- API Testing: Postman