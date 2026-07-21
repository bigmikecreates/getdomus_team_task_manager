# GetDomus Team Task Manager — Project Specification

## 1. Overview

A production-oriented task management web application designed for distributed engineering teams. Supports multi-developer assignment, timezone awareness, and role-based access control.

## 2. Tech Stack

| Layer | Technology | Version |
|---|---|---|
| Frontend | Next.js + TypeScript | 14+ (App Router) |
| UI | Tailwind CSS | Latest |
| State/Data | React Query (TanStack Query) | Latest |
| Backend | FastAPI (Python) | Latest |
| ORM | SQLAlchemy (async) | 2.0+ |
| Migrations | Alembic | Latest |
| Validation | Pydantic v2 | Latest |
| Database | PostgreSQL | 15+ |
| Auth | JWT (python-jose) + bcrypt | — |
| Timezone | pytz / zoneinfo | — |
| Containerization | Docker + Docker Compose | — |
| CI/CD | GitHub Actions | — |
| Docs | MKDocs + Material theme | — |

## 3. Domain Model

### Developer

| Field | Type | Notes |
|---|---|---|
| id | UUID | Primary key |
| name | String | Required |
| email | String | Unique, required |
| timezone | String | IANA identifier (e.g., `Europe/London`) |
| role | Enum | `admin`, `manager`, `developer` |
| working_hours_start | Time | Optional |
| working_hours_end | Time | Optional |
| last_seen_at | DateTime | For online/offline foundation |
| created_at | DateTime | Auto |
| updated_at | DateTime | Auto |

### User (Auth)

| Field | Type | Notes |
|---|---|---|
| id | UUID | Primary key |
| email | String | Unique, required |
| password_hash | String | bcrypt |
| role | Enum | `admin`, `manager`, `developer` |
| developer_id | UUID | FK → Developer (optional, links auth to profile) |
| created_at | DateTime | Auto |

### Task

| Field | Type | Notes |
|---|---|---|
| id | UUID | Primary key |
| title | String | Required |
| description | Text | Optional |
| status | Enum | `todo`, `in_progress`, `in_review`, `done` |
| priority | Enum | `low`, `medium`, `high`, `critical` |
| due_date | DateTime | Optional |
| created_by | UUID | FK → User |
| created_at | DateTime | Auto |
| updated_at | DateTime | Auto |

### TaskAssignment

| Field | Type | Notes |
|---|---|---|
| task_id | UUID | FK → Task |
| developer_id | UUID | FK → Developer |
| assigned_at | DateTime | Auto |

Composite primary key: `(task_id, developer_id)`

## 4. API Endpoints

### Auth

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login, returns JWT |
| GET | `/api/auth/me` | Current user profile |

### Tasks

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/tasks` | All | List tasks (filterable by status, priority, assignee) |
| POST | `/api/tasks` | admin, manager | Create task |
| GET | `/api/tasks/{id}` | All | Get task detail |
| PUT | `/api/tasks/{id}` | admin, manager | Update task |
| POST | `/api/tasks/{id}/assign` | admin, manager | Assign developer(s) |
| DELETE | `/api/tasks/{id}/assignments/{dev_id}` | admin, manager | Unassign developer |

### Developers

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/developers` | All | List developers with local time |
| POST | `/api/developers` | admin | Create developer profile |
| PUT | `/api/developers/{id}` | admin | Update developer |
| GET | `/api/developers/{id}/availability` | All | Check working hours status |

### Dashboard

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/dashboard/stats` | Task counts by status, priority |
| GET | `/api/dashboard/overview` | Summary data for dashboard cards |

## 5. Backend Structure

```
backend/
  api/
    __init__.py
    v1/
      __init__.py
      auth.py
      tasks.py
      developers.py
      dashboard.py
  services/
    __init__.py
    auth_service.py
    task_service.py
    developer_service.py
    dashboard_service.py
  repositories/
    __init__.py
    task_repository.py
    developer_repository.py
    user_repository.py
  models/
    __init__.py
    base.py
    developer.py
    user.py
    task.py
    task_assignment.py
  schemas/
    __init__.py
    auth.py
    task.py
    developer.py
    dashboard.py
  core/
    __init__.py
    config.py
    security.py
    dependencies.py
    database.py
  main.py
```

## 6. Frontend Structure

```
frontend/
  app/
    layout.tsx
    page.tsx              ← Dashboard
    login/page.tsx
    register/page.tsx
    tasks/
      page.tsx            ← Task list / board
      [id]/page.tsx       ← Task detail / edit
    developers/
      page.tsx            ← Developer list
  components/
    ui/                   ← Shared UI components (Button, Card, Modal, etc.)
    layout/               ← Sidebar, Header, etc.
    tasks/                ← TaskCard, TaskForm, TaskBoard, etc.
    developers/           ← DeveloperCard, AvailabilityBadge, etc.
    dashboard/            ← StatsCard, OverviewChart, etc.
  hooks/
    useAuth.ts
    useTasks.ts
    useDevelopers.ts
    useDashboard.ts
  lib/
    api.ts                ← API client (fetch wrapper)
    auth.ts               ← JWT token management
    utils.ts              ← Timezone helpers, formatters
  types/
    index.ts              ← TypeScript interfaces matching backend schemas
```

## 7. Sprint Plan

### Sprint 1: Backend Foundation & Database

**Branch:** `feature/backend-foundation`
**Goal:** Working API with data models, running locally against Dockerized Postgres.

| # | Task | Detail |
|---|---|---|
| 1 | Configure `pyproject.toml` | FastAPI, SQLAlchemy, Alembic, Pydantic, uvicorn, psycopg2, python-jose, bcrypt, pytz, python-dotenv |
| 2 | Backend project structure | Create directory layout as defined in Section 5 |
| 3 | Core config | `config.py` (env vars, settings), `database.py` (async engine, session), `security.py` (JWT helpers) |
| 4 | Models | Developer, User, Task, TaskAssignment with relationships |
| 5 | Alembic setup + initial migration | Generate and apply migration |
| 6 | Schemas | Pydantic request/response models for all entities |
| 7 | Repository layer | CRUD operations for each model |
| 8 | Service layer | Business logic (create task, assign developer, etc.) |
| 9 | API routes | Auth, Tasks, Developers, Dashboard endpoints |
| 10 | Seed script | Sample developers + tasks + users for local dev |
| 11 | Docker Compose | PostgreSQL container only (no app containerization) |
| 12 | Test infrastructure | pytest, pytest-asyncio, httpx, factory_boy, conftest.py with fixtures (test client, test DB session, auth helpers) |
| TDD | Model tests | Write tests for Developer, User, Task, TaskAssignment relationships and constraints alongside model creation |
| TDD | API endpoint tests | Write tests for each endpoint (happy path + error cases) before implementing the endpoint |
| TDD | Service layer tests | Write tests for business logic (task creation, assignment, status transitions) before implementing |

**DoD:** API runs, all endpoints return correct data, DB migrations apply cleanly, all endpoints have passing TDD tests, model and service tests exist.

### Sprint 2: Authentication & Frontend Shell

**Branch:** `feature/auth-frontend`
**Goal:** RBAC auth system + Next.js app with basic task CRUD.

| # | Task | Detail |
|---|---|---|
| 1 | User model + auth endpoints | Register, login, JWT token generation |
| 2 | `require_role()` dependency | FastAPI dependency for role-based route protection |
| 3 | Apply auth to all existing endpoints | Protect routes per Section 4 |
| 4 | Scaffold Next.js | TypeScript, App Router, Tailwind CSS, React Query |
| 5 | API client + auth hooks | Fetch wrapper with JWT header injection |
| 6 | Login + register pages | Form UI, redirect on success |
| 7 | Layout shell | Sidebar nav, "Logged in as X (role)" header |
| 8 | Task list page | Table view of tasks with status, priority, due date |
| 9 | Task create/edit form | Form to create + update tasks |
| 10 | Developer list page | Read-only list with name, email, timezone |
| 11 | Role-aware navigation | Admin sees developer management, developer sees only assigned tasks |
| 12 | Seed script update | Create admin, manager, developer users |
| 13 | Frontend test setup | Vitest, @testing-library/react, msw for API mocking |
| TDD | Auth endpoint tests | Test register, login, JWT validation, role enforcement before implementing |
| TDD | Role middleware tests | Test `require_role()` with each role before implementing |
| Test | Frontend auth tests | Behavior-focused tests for login form, register form, role-based rendering |

**DoD:** Can register, login, create/edit/view tasks. Role-based nav works. Auth endpoints have TDD tests. Frontend auth flow has behavior tests.

### Sprint 3: Dashboard & Multi-Assignment

**Branch:** `feature/dashboard-assignments`
**Goal:** Dashboard with stats + ability to assign multiple developers to tasks.

| # | Task | Detail |
|---|---|---|
| 1 | Dashboard stats API | Task counts by status, priority, assignee |
| 2 | Dashboard UI | Stats cards + summary view |
| 3 | Task board view | Kanban-style columns: To Do, In Progress, In Review, Done |
| 4 | Multi-assignment API | Wire up assign/unassign endpoints |
| 5 | Multi-select assignment UI | Dropdown/multi-select on task detail |
| 6 | Assigned developers display | Show avatars/names on task cards |
| 7 | Filtering + search | Filter tasks by status, priority, assignee |
| TDD | Dashboard stats tests | Test stats calculation (counts by status, priority, assignee) before implementing dashboard endpoint |
| TDD | Multi-assignment tests | Test assign/unassign logic, duplicate assignment prevention before implementing |
| Test | Frontend assignment tests | Behavior tests: "allows manager to assign multiple developers to a task", "shows assigned developers on task card" |

**DoD:** Dashboard shows stats. Kanban board works. Multi-assignment functional. Dashboard and assignment endpoints have TDD tests.

### Sprint 4: Timezones, Online/Offline Foundation & Polish

**Branch:** `feature/timezones-polish`
**Goal:** Developer timezone awareness + UX polish + online/offline groundwork.

| # | Task | Detail |
|---|---|---|
| 1 | Developer local time display | Show each developer's current local time using IANA timezone |
| 2 | Due date timezone context | Show due dates with timezone awareness |
| 3 | `last_seen_at` field + heartbeat endpoint | Foundation for online/offline status |
| 4 | WebSocket skeleton (stretch) | `/ws/presence` endpoint if time permits |
| 5 | Presence indicator UI (stretch) | Green/red dot next to developer name |
| 6 | Working hours indicator | Visual badge: within hours / outside hours |
| 7 | Empty states | "No tasks yet", "No developers assigned", etc. |
| 8 | Loading states | Skeletons / spinners for all async operations |
| 9 | Error handling | Toast notifications, error boundaries |
| 10 | Responsive design | Mobile-friendly layouts |
| TDD | Timezone tests | Test IANA timezone conversion, due date display across timezones |
| TDD | Availability tests | Test working hours calculation, edge cases (overnight hours, DST) before implementing indicator |
| Test | Frontend behavior tests | Test empty states render correctly, error boundaries catch failures, loading states display |

**DoD:** Timezones display correctly. UI is polished. Online/offline foundation in place. Timezone and availability logic has TDD tests.

### Sprint 5: Documentation, Containerization, CI/CD & Deploy

**Branch:** `feature/deploy-docs`
**Goal:** Production deployment with documentation site.

| # | Task | Detail |
|---|---|---|
| 1 | `docs/spec.md` | Full project specification |
| 2 | `docs/architecture.md` | System architecture + diagram |
| 3 | `docs/decisions.md` | Key architectural decisions |
| 4 | `docs/deployment.md` | Deployment guide |
| 5 | `docs/setup.md` | Local development setup |
| 6 | `docs/api.md` | API reference |
| 7 | MKDocs setup | `mkdocs.yml` + Material theme |
| 8 | GitHub Pages deployment | CI/CD step to build + publish docs |
| 9 | Dockerfile (backend) | Multi-stage Python build |
| 10 | Dockerfile (frontend) | Multi-stage Node build |
| 11 | docker-compose.yml | Full stack: backend + frontend + PostgreSQL |
| 12 | GitHub Actions CI | Lint + test on PR to `main` |
| 13 | GitHub Actions CD | Deploy frontend to Vercel, backend to Railway on merge to `main` |
| 14 | Deploy to production | Vercel (frontend), Railway (backend), Neon (database) |
| 15 | README.md | Project overview, quick start, links to docs |

**DoD:** App deployed and accessible. CI/CD runs on PRs. Documentation site live on GitHub Pages.

## 8. Deployment Architecture

```
┌──────────────────────────────────────────────────────────┐
│                      INTERNET                            │
└─────┬────────────────────────┬───────────────────────────┘
      │                        │
┌─────▼─────┐           ┌──────▼──────┐
│  Vercel   │           │   GitHub    │
│ (Frontend)│           │   Pages     │
│  Next.js  │           │  (Docs)     │
└─────┬─────┘           └─────────────┘
      │ API calls (CORS)
┌─────▼─────┐
│  Railway  │
│ (Backend) │
│  FastAPI  │
└─────┬─────┘
      │ DATABASE_URL (SSL)
┌─────▼─────┐
│   Neon    │
│(Database) │
│ PostgreSQL│
└───────────┘
```

| Component | Service | Purpose |
|---|---|---|
| Frontend | Vercel | Next.js hosting, preview deployments |
| Backend | Railway | FastAPI hosting, env var management |
| Database | Neon | Serverless PostgreSQL |
| Documentation | GitHub Pages | MKDocs site |
| CI/CD | GitHub Actions | Lint, test, build, deploy |

## 9. Deferred Features (Future Enhancements)

| Feature | Status | Notes |
|---|---|---|
| Full real-time WebSocket presence | Deferred | Foundation in Sprint 4, full impl if time |
| File attachments on tasks | Deferred | Clean extension point |
| Working hours精细 logic | Deferred | Basic indicator in Sprint 4 |
| OAuth/external auth providers | Deferred | Out of scope for v1 |

## 10. Branching Strategy

```
main
  ├── feature/backend-foundation    (Sprint 1)
  ├── feature/auth-frontend         (Sprint 2)
  ├── feature/dashboard-assignments (Sprint 3)
  ├── feature/timezones-polish      (Sprint 4)
  └── feature/deploy-docs           (Sprint 5)
```

Each feature branch merges to `main` via PR. No `develop` integration branch — solo project, unnecessary ceremony.

## 11. Development Methodology

### Specification-Driven Development (SDD)

The project follows SDD — `docs/spec.md` is the single source of truth.
Implementation follows the spec. Code is written to satisfy the specification,
not the other way around.

### Test-Driven Development (TDD) — Backend

Backend development follows strict TDD:

1. **Write the test first** — define expected behavior via a failing test
2. **Implement** — write the minimum code to pass
3. **Refactor** — clean up while keeping tests green

**Scope of backend TDD:**
- All API endpoints (happy path + error cases)
- Service layer business logic
- Model relationships and constraints
- Auth middleware and role-based access

**Tools:** pytest, pytest-asyncio, httpx (async test client), factory_boy

### Behavior-Focused Testing — Frontend

Frontend tests use a BDD-inspired style without formal Gherkin/Cucumber.
Tests describe **user behavior**, not implementation details.

**Naming convention:** test names describe the user's action and expected outcome.

```typescript
// Good (behavior-focused):
it('allows a manager to create a task with a title and priority', async () => { ... })
it('prevents a developer from creating tasks', async () => { ... })

// Avoid (implementation-focused):
it('renders TaskForm', () => { ... })
it('calls onSubmit handler', () => { ... })
```

**Scope of frontend tests (target: 30-50% coverage):**
- Custom hooks (useAuth, useTasks, etc.)
- Form validation and submission logic
- Role-based rendering (admin vs developer views)
- Critical user flows (login, create task, assign developer)

**Tools:** Vitest, @testing-library/react, msw (API mocking)

**Not tested:**
- CSS/Tailwind styling
- Third-party library internals
- Page layout composition
