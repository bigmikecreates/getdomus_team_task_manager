# Architecture

## System Overview

```mermaid
graph TB
    subgraph Frontend["Frontend (Next.js 16)"]
        AppRouter["App Router"]
        ReactQuery["TanStack Query"]
        TailwindCSS["Tailwind CSS 4"]
    end

    subgraph Backend["Backend (FastAPI)"]
        APIRoutes["API Routes"]
        Services["Services"]
        Repositories["Repositories"]
        Models["SQLAlchemy Models"]
    end

    subgraph Database["Database"]
        PostgreSQL["PostgreSQL 16"]
        Alembic["Alembic Migrations"]
    end

    subgraph External["External"]
        JWT["JWT Auth"]
        Timezones["IANA Timezones"]
    end

    AppRouter --> ReactQuery
    ReactQuery -->|"HTTP + JWT"| APIRoutes
    APIRoutes --> Services
    Services --> Repositories
    Repositories --> Models
    Models --> PostgreSQL
    Alembic --> PostgreSQL
    APIRoutes --> JWT
    Services --> Timezones
```

## Tech Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| Frontend | Next.js | 16.2.10 | React framework (App Router) |
| UI | Tailwind CSS | 4 | Utility-first styling |
| Data | TanStack Query | 5.x | Server state management |
| Backend | FastAPI | Latest | Async REST API |
| ORM | SQLAlchemy | 2.0+ | Async database access |
| Migrations | Alembic | Latest | Schema versioning |
| Database | PostgreSQL | 16 | Persistent storage |
| Auth | JWT | — | python-jose + bcrypt |
| Timezone | zoneinfo | — | IANA timezone support |

## Backend Structure

```
backend/
  api/v1/            Route handlers
    auth.py          POST /register, /login, GET /me
    tasks.py         CRUD + assign/unassign
    developers.py    CRUD + availability
    dashboard.py     Stats + overview
    presence.py      Heartbeat endpoint
  services/          Business logic
    auth_service.py
    task_service.py
    developer_service.py
    dashboard_service.py
    presence_service.py
  repositories/      Database queries
    task_repository.py
    developer_repository.py
    user_repository.py
  models/            SQLAlchemy ORM models
    user.py
    developer.py
    task.py
    task_assignment.py
  schemas/           Pydantic request/response
    auth.py
    task.py
    developer.py
    dashboard.py
  core/              Infrastructure
    config.py        Environment settings
    database.py      Async engine + session
    security.py      JWT + password hashing
    dependencies.py  Auth + role dependencies
    timezone_utils.py  IANA timezone conversion
  main.py            FastAPI app entry point
```

## Frontend Structure

```
frontend/src/
  app/
    (auth)/          Authentication pages
      login/
      register/
    (dashboard)/     Main app pages
      page.tsx       Dashboard
      tasks/         Task list, create, edit, detail
      developers/    Developer list, create
  components/        Shared components
    sidebar.tsx
    error-boundary.tsx
    developer-multiselect.tsx
  lib/
    api.ts           API client (fetch wrapper)
    auth.tsx         AuthProvider + useAuth hook
    labels.ts        Shared status/priority labels
  __tests__/         Frontend tests + MSW mocks
```

## Data Flow

```mermaid
sequenceDiagram
    participant B as Browser
    participant F as Next.js Frontend
    participant A as FastAPI Backend
    participant D as PostgreSQL

    B->>F: User action
    F->>F: React Query mutation
    F->>A: HTTP + JWT Bearer token
    A->>A: Validate auth + roles
    A->>A: Service layer logic
    A->>D: Async SQLAlchemy query
    D-->>A: Result
    A-->>F: JSON response
    F-->>B: UI update
```

## Auth Flow

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant A as Backend

    U->>F: Enter credentials
    F->>A: POST /api/auth/login
    A->>A: Validate password (bcrypt)
    A->>A: Generate JWT (HS256)
    A-->>F: { access_token, token_type }
    F->>F: Store token in localStorage
    F->>F: Fetch user profile (GET /api/auth/me)

    Note over F,A: Subsequent requests
    F->>A: Authorization: Bearer <token>
    A->>A: Decode JWT, check role
    A-->>F: Protected resource
```

## RBAC Permissions

| Endpoint | Admin | Manager | Developer |
|----------|:-----:|:-------:|:---------:|
| `POST /api/tasks` | ✅ | ✅ | ❌ |
| `PUT /api/tasks/{id}` | ✅ | ✅ | ❌ |
| `DELETE /api/tasks/{id}` | ✅ | ✅ | ❌ |
| `POST /api/tasks/{id}/assign` | ✅ | ✅ | ❌ |
| `POST /api/developers` | ✅ | ❌ | ❌ |
| `PUT /api/developers/{id}` | ✅ | ❌ | ❌ |
| `DELETE /api/developers/{id}` | ✅ | ❌ | ❌ |
| All read endpoints | ✅ | ✅ | ✅ |
