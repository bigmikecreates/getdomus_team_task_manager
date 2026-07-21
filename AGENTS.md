# AGENTS.md

## Project

GetDomus Team Task Manager — task management app for distributed teams.
Spec: `docs/spec.md`

## Tech Stack

- Backend: FastAPI + SQLAlchemy (async) + PostgreSQL
- Frontend: Next.js 14 (App Router) + TypeScript + Tailwind CSS + React Query
- Auth: JWT with RBAC (admin, manager, developer)
- Docs: MKDocs + Material theme

## Sprint Workflow

- Before starting a sprint, verify the corresponding GitHub Issue exists
- If it does not exist, create it with the task checklist from `docs/spec.md` Section 7
- Create and checkout the sprint branch before any implementation: `git checkout -b feature/<sprint-name>`
- Reference `docs/spec.md` Section 7 for the current sprint plan
- Track progress via the GitHub Issue checklist (check off tasks as completed)
- Stay within current sprint scope unless explicitly told otherwise
- Branch naming: `feature/<sprint-name>` (e.g., `feature/backend-foundation`)
- When sprint is complete, open a PR referencing the issue (e.g., "Closes #1")
- After merging a PR, do NOT delete the feature branch — keep all branches preserved as an audit trail for presentation and review purposes

## PR Workflow

- All changes go through PRs — no direct pushes to `main`
- After merging a PR, keep the feature branch (do not delete)
- Preserve full commit history on feature branches

## Manual Review Checklist

After raising a PR, present the following to the user before merging. The user runs these checks themselves to verify the sprint is complete.

### 1. Automated Checks — Run These

Provide the exact commands the user should run in the repo root (or correct subdirectory) with expected outcomes.

```bash
# Backend tests
pytest -v
# Expect: all tests passing, 0 warnings

# Frontend tests
cd frontend && npm run test
# Expect: all tests passing

# Frontend build
cd frontend && npm run build
# Expect: clean build, no errors, all routes compile
```

### 2. Manual Verification — Check These

Start the database, seed it, then start both dev servers:
```bash
# 1. Start PostgreSQL
docker compose up -d

# 2. Seed the database (idempotent — safe to run multiple times)
python -m backend.seed

# 3. Start backend
uvicorn backend.main:app --reload

# 4. Start frontend (separate terminal)
cd frontend && npm run dev
```

Open `http://localhost:3000` and verify the new features by performing step-by-step actions. Format as a numbered table: Step | Action | Expected Result.

### 3. Code Changes — Files Changed

List every file changed with a one-line summary of what changed. Group by backend/frontend/tests.

### 4. Issue Checklist

Confirm all items in the GitHub Issue checklist are checked off. List the issue URL.

### 5. Deferred Items

List any items explicitly deferred from the sprint, or state "None."

## Development Methodology

- **SDD:** `docs/spec.md` is the source of truth. Implementation follows spec.
- **Backend TDD:** Write tests first (red -> green -> refactor). All API endpoints, services, and models must have tests before implementation is considered complete.
- **Frontend:** Behavior-focused tests (BDD-inspired naming). Tests describe user actions, not implementation. Target 30-50% coverage on critical paths.

## Commands

- Backend: `uvicorn backend.main:app --reload`
- Frontend: `npm run dev` (in frontend/)
- DB migrations: `alembic upgrade head`
- Backend tests: `pytest`
- Frontend tests: `npm run test` (in frontend/)

## Code Conventions

- Backend: follow existing patterns in the directory structure
- Frontend: TypeScript strict mode, components in feature folders
- Commit messages: conventional commits (`feat:`, `fix:`, `test:`, `docs:`)
