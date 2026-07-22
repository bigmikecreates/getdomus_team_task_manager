# API Reference

> Auto-generated from FastAPI's OpenAPI schema.
> Run `python scripts/generate_api_docs.py` to regenerate (requires running backend server).

Interactive docs available at: `<backend-url>/docs`

## Overview

The API follows REST conventions. All endpoints return JSON.

**Base URL:** `http://localhost:8000` (development)

**Authentication:** JWT Bearer token in `Authorization` header.

## Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/health` | None | Health check |
| `POST` | `/api/auth/register` | None | Register new user |
| `POST` | `/api/auth/login` | None | Login, returns JWT |
| `GET` | `/api/auth/me` | Bearer | Get current user |
| `GET` | `/api/tasks` | Bearer | List all tasks |
| `POST` | `/api/tasks` | Bearer (admin/manager) | Create task |
| `GET` | `/api/tasks/{task_id}` | Bearer | Get task detail |
| `PUT` | `/api/tasks/{task_id}` | Bearer (admin/manager) | Update task |
| `DELETE` | `/api/tasks/{task_id}` | Bearer (admin/manager) | Delete task |
| `POST` | `/api/tasks/{task_id}/assign` | Bearer (admin/manager) | Assign developers |
| `DELETE` | `/api/tasks/{task_id}/assignments/{dev_id}` | Bearer (admin/manager) | Unassign developer |
| `GET` | `/api/developers` | Bearer | List developers with availability |
| `POST` | `/api/developers` | Bearer (admin) | Create developer profile |
| `PUT` | `/api/developers/{developer_id}` | Bearer (admin) | Update developer |
| `DELETE` | `/api/developers/{developer_id}` | Bearer (admin) | Delete developer |
| `GET` | `/api/dashboard/stats` | Bearer | Task statistics |
| `GET` | `/api/dashboard/overview` | Bearer | Full dashboard overview |
| `POST` | `/api/presence/heartbeat` | Bearer | Record heartbeat |

## Regenerating This Page

```bash
# 1. Start the backend server
uvicorn backend.main:app --reload

# 2. Run the generator (in a separate terminal)
python scripts/generate_api_docs.py

# 3. Commit the updated file
git add docs/technical/api/reference.md
git commit -m "docs: update API reference"
```
