# Local Development Setup

## Prerequisites

- Python 3.14+
- Node.js 20+
- Docker & Docker Compose
- Git

## 1. Clone & Install

```bash
git clone https://github.com/bigmikecreates/getdomus_team_task_manager.git
cd getdomus_team_task_manager
```

### Backend

```bash
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (macOS/Linux)
source .venv/bin/activate

pip install -e ".[dev]"
```

### Frontend

```bash
cd frontend
npm install
cd ..
```

## 2. Start Database

```bash
docker compose up -d
```

Verify it's running:

```bash
docker compose ps
```

## 3. Configure Environment

The app uses these environment variables (defaults work for local dev):

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql+asyncpg://postgres:postgres@localhost:5432/taskmanager` | Database connection |
| `SECRET_KEY` | `dev-secret-key-change-in-production` | JWT signing key |
| `ALLOWED_ORIGINS` | `["http://localhost:3000"]` | CORS allowed origins |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | JWT token lifetime |

Create a `.env` file to override defaults:

```bash
cp .env.example .env
```

## 4. Run Migrations & Seed

```bash
# Apply database migrations
alembic upgrade head

# Seed with sample data (idempotent — safe to run multiple times)
python -m backend.seed
```

## 5. Start Dev Servers

**Terminal 1 — Backend:**

```bash
uvicorn backend.main:app --reload
```

**Terminal 2 — Frontend:**

```bash
cd frontend && npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

## 6. Verify

- Swagger docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Health check: [http://localhost:8000/health](http://localhost:8000/health)

## Test Accounts

| Email | Password | Role |
|-------|----------|------|
| admin@example.com | admin123 | admin |
| manager@example.com | manager123 | manager |
| dev@example.com | dev123 | developer |

## Troubleshooting

### Database connection refused

Ensure Docker is running and the `db` service is healthy:

```bash
docker compose up -d
docker compose ps
```

### Migration errors

Reset the database (loses all data):

```bash
docker compose down -v
docker compose up -d
alembic upgrade head
python -m backend.seed
```

### Port already in use

```bash
# Find process using port 8000 (backend)
netstat -ano | findstr :8000

# Find process using port 3000 (frontend)
netstat -ano | findstr :3000
```
