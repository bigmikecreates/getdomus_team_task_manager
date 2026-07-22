# Testing

## Overview

| Layer | Framework | Count | Style |
|-------|-----------|-------|-------|
| Backend | pytest + pytest-asyncio | 111 | TDD (red → green → refactor) |
| Frontend | Vitest + React Testing Library + MSW | 27 | Behavior-focused (BDD-inspired) |

## Running Tests

### Backend

```bash
# Run all tests
python -m pytest -v

# Run a specific test file
python -m pytest backend/tests/test_api/test_tasks.py -v

# Run tests matching a pattern
python -m pytest -k "delete" -v
```

Backend tests use **SQLite in-memory** (via `aiosqlite`) — no Docker required.

### Frontend

```bash
cd frontend

# Run all tests
npm run test

# Run tests in watch mode
npm run test:watch
```

Frontend tests use **MSW (Mock Service Worker)** to mock API responses.

## TDD Workflow (Backend)

All backend code follows strict TDD:

```bash
# 1. Write the test first
# 2. Run it — see it fail (red)
python -m pytest backend/tests/test_api/test_new_endpoint.py -v

# 3. Implement the minimum code to pass (green)
# 4. Run again — see it pass
python -m pytest -v

# 5. Refactor while keeping tests green
```

### What Gets Tested

- **API endpoints** — Happy path + error cases (401, 403, 404, 422)
- **Services** — Business logic, edge cases, error handling
- **Repositories** — Database queries, constraints
- **Models** — Relationships, defaults, unique constraints

### Test Structure

```
backend/tests/
  conftest.py              # Fixtures (test client, DB session, auth helpers)
  test_api/                # API endpoint tests
    test_auth.py
    test_tasks.py
    test_developers.py
    test_dashboard.py
    test_presence.py
  test_services/           # Service + repository tests
    test_auth_service.py
    test_task_service.py
    test_task_repository.py
    test_developer_repository.py
    test_dashboard_service.py
    test_timezone_utils.py
    test_presence_service.py
  test_models/
    test_models.py
```

## Frontend Testing

### Behavior-Focused Style

Tests describe user actions, not implementation:

```typescript
// Good — describes what the user does
it("allows a manager to create a task with a title and priority", async () => { ... })
it("prevents a developer from creating tasks", async () => { ... })

// Avoid — describes implementation
it("renders TaskForm", () => { ... })
it("calls onSubmit handler", () => { ... })
```

### Test Structure

```
frontend/src/__tests__/
  login.test.tsx                 # Auth flow tests
  register.test.tsx
  dashboard.test.tsx             # Dashboard rendering
  task-list.test.tsx             # Task list behavior
  developers-availability.test.tsx  # Availability display
  error-boundary.test.tsx        # Error handling
  empty-states.test.tsx          # Empty state rendering
  mocks/
    server.ts                    # MSW server setup
    handlers.ts                  # API mock handlers
```

### MSW Mock Handlers

API responses are mocked in `frontend/src/__tests__/mocks/handlers.ts`. To test a specific scenario:

```typescript
server.use(
  http.get("*/api/tasks", () => {
    return HttpResponse.json({ tasks: [...], total: 2 });
  })
);
```

## Coverage

Target: **30–50%** on critical paths (auth, task CRUD, assignment).

Check coverage:

```bash
cd frontend && npm run test -- --coverage
```
