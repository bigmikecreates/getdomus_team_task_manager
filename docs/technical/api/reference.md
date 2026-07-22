# API Reference

> Interactive Swagger docs are available at: `<backend-url>/docs`

**Base URL:** `https://getdomusteamtaskmanager-production.up.railway.app`

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
| `DELETE` | `/api/developers/{developer_id}` | Bearer (admin) | Delete developer |
| `GET` | `/api/dashboard/stats` | Bearer | Task statistics |
| `GET` | `/api/dashboard/overview` | Bearer | Full dashboard overview |
| `POST` | `/api/presence/heartbeat` | Bearer | Record heartbeat |

## RBAC Permissions

| Endpoint | Admin | Manager | Developer |
|----------|:-----:|:-------:|:---------:|
| Create/Update/Delete tasks | ✅ | ✅ | ❌ |
| Assign/Unassign developers | ✅ | ✅ | ❌ |
| Create/Delete developers | ✅ | ❌ | ❌ |
| All read endpoints | ✅ | ✅ | ✅ |
