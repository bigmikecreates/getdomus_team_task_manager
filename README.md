# GetDomus Team Task Manager

Task management app for distributed engineering teams. Supports multi-developer assignment, timezone awareness, and role-based access control.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 16 + TypeScript + Tailwind CSS |
| Backend | FastAPI + SQLAlchemy (async) |
| Database | PostgreSQL 16 |
| Auth | JWT with RBAC |
| Docs | MKDocs + Material theme |

## Quick Start

### Prerequisites

- Python 3.14+
- Node.js 20+
- Docker & Docker Compose

### Setup

```bash
# Clone
git clone https://github.com/bigmikecreates/getdomus_team_task_manager.git
cd getdomus_team_task_manager

# Backend
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -e ".[dev]"

# Frontend
cd frontend && npm install && cd ..

# Database
docker compose up -d
alembic upgrade head
python -m backend.seed

# Start servers
uvicorn backend.main:app --reload          # Backend (port 8000)
cd frontend && npm run dev                 # Frontend (port 3000)
```

Open [http://localhost:3000](http://localhost:3000)

### Test Accounts

| Email | Password | Role |
|-------|----------|------|
| admin@example.com | admin123 | admin |
| manager@example.com | manager123 | manager |
| dev@example.com | dev123 | developer |

## Testing

```bash
# Backend (111 tests)
python -m pytest -v

# Frontend (27 tests)
cd frontend && npm run test
```

## Documentation

Full documentation is available at the [docs](docs/index.md) folder, or deploy locally with MKDocs:

```bash
pip install mkdocs-material mkdocs-mermaid2-plugin
mkdocs serve
```

## Project Structure

```
getdomus_team_task_manager/
  backend/          FastAPI backend (models, services, API routes)
  frontend/         Next.js frontend (App Router, TypeScript)
  docs/             Documentation (MKDocs)
  alembic/          Database migrations
  scripts/          Utility scripts
  docker-compose.yml
```

## License

Private — GetDomus Graduate Full-Stack Technical Assessment
