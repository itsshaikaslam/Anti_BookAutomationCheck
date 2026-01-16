# API & Server Actions

## Generation Actions
- `POST /api/generations`: Start single ebook generation.
- `POST /api/generations/batch`: Start batch generation (up to 10 topics).
- `POST /api/generations/{id}/cancel`: Abort in-progress task.

## Informational Endpoints
- `GET /api/generations`: List user's generation history.
- `GET /api/generations/{id}`: Detailed logs, metrics, and links for a specific ebook.
- `GET /api/admin/stats`: Aggregate system metrics (total generated, cost, success rate).

## Detailed Management Endpoints
- `GET /api/generations/{id}/chapters`: List all generated chapters and their statuses.
- `GET /api/generations/{id}/chapters/{chapter_number}`: Retrieve content/markdown for a specific chapter.
- `GET /api/generations/{id}/infographics`: List all generated infographics with metadata.
- `GET /api/generations/{id}/report`: Download the comprehensive Quality & Fact-verification PDF report.
- `POST /api/generations/{id}/regenerate/{chapter_number}`: Re-trigger generation for a specific chapter (Manual intervention fallback).

## Real-time Communication (WebSocket)
- **Namespace**: `/ws/generation`
- **Events**:
  - `progress_update`: Emitted by Celery worker via Redis pub/sub.
  - `chapter_completed`: Notifies the UI as each parallel chapter finishes.
  - `log_added`: Live stream of agent internal logs.
  - `generation_error`: Critical failure notifications.

## Background worker integration
All heavy lifting (Agent orchestration) is delegated to Celery. The FastAPI server handles request validation and database persistence of initial states before dispatching tasks.
