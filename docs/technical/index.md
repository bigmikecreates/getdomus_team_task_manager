# Technical Guide

This guide covers development setup, architecture, testing, and deployment.

## Development Approach

This project was built using a sprint-based methodology with test-driven development (TDD) on the backend and behavior-focused testing on the frontend.

**Backend TDD:** Each API endpoint, service method, and repository function was written test-first. Tests run against an in-memory SQLite database, keeping the feedback loop fast and the CI pipeline dependency-free. The result is 111 tests covering the full API surface, business logic, and data layer.

**Frontend BDD:** Tests describe user actions (e.g., "renders email and password fields", "allows user to type email and password") rather than implementation details. MSW mocks the API layer, allowing tests to verify behavior without a running backend. The result is 38 tests covering authentication, dashboard, task management, developer availability, and error handling.

**Layered Architecture:** The backend follows a Repository → Service → Router pattern. Repositories handle database queries, services contain business logic, and routers handle HTTP concerns. This separation makes each layer independently testable.

**Sprint Cadence:** Development was divided into 5 sprints, each delivered as a pull request with passing CI:

| Sprint | Focus |
|--------|-------|
| 1 | Backend foundation — models, repos, services, API routes, migrations, seed data |
| 2 | Frontend shell — login, register, dashboard, task CRUD, developer list |
| 3 | Unified dashboard — stats, task filtering, sidebar navigation |
| 4 | Polish — timezone utils, presence, delete operations, sortable columns, shared labels |
| 5 | Production readiness — documentation, containerization, CI/CD |

## Contents

| Topic | Description |
|-------|-------------|
| [Local Setup](setup.md) | Get the app running on your machine |
| [Testing](testing.md) | Run tests, TDD workflow |
| [Contributing](contributing.md) | Code conventions, PR workflow |
| [Deployment](deployment.md) | Production setup (Vercel, Railway, Neon) |
| [Architecture](architecture.md) | System design, tech stack, diagrams |
| [Decisions](decisions.md) | Key architectural choices and rationale |
| [Assumptions](assumptions.md) | Assumptions made during development |
| [API Reference](api/reference.md) | Endpoint summary |
