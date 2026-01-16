# Project Setup & Configuration

## Environment Requirements
| Requirement | Specification |
|-------------|---------------|
| OS | Linux (Ubuntu 22.04 LTS recommended) / Docker |
| RAM | 32 GB (16 GB min) |
| CPU | 8+ Cores |
| Storage | 200 GB SSD |

## Tech Stack
- **Backend**: FastAPI (Python 3.11+)
- **Frontend**: React 18+ (Vite, TypeScript, Tailwind CSS)
- **Task Queue**: Celery + Redis
- **Database**: PostgreSQL 15+
- **File Storage**: MinIO (Internal) + Google Drive API (External)
- **AI Services**: Ollama (Local LLMs), Stable Diffusion XL Lightning (Images)
- **PDF Engine**: WeasyPrint / ReportLab

## Development Setup
1. **Clone & Environment**:
   ```bash
   git clone <repo>
   cd ebook-system
   cp .env.example .env
   ```
2. **Docker Compose**:
   ```bash
   docker-compose up -d
   ```
3. **Ollama Installation**:
   - Install Ollama on host or container.
   - Pull models: `ollama pull llama3.1`, `ollama pull mistral`, `ollama pull sd-xl-lightning`.

## Key Dependencies
- `fastapi`, `uvicorn`: API Framework.
- `celery`, `redis`: Distributed task processing.
- `sqlalchemy`, `psycopg2-binary`: Database ORM.
- `weasyprint`, `jinja2`: PDF generation templates.
- `languagetool`: Multi-language grammar checking.
- `pydrive2`: Google Drive integration.
