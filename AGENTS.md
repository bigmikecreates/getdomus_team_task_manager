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
