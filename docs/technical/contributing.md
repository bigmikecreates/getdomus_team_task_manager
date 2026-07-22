# Contributing

## Branching Strategy

```
main
  ├── feature/backend-foundation    (Sprint 1)
  ├── feature/auth-frontend         (Sprint 2)
  ├── feature/dashboard-assignments (Sprint 3)
  ├── feature/timezones-polish      (Sprint 4)
  └── feature/deploy-docs           (Sprint 5)
```

- All changes go through PRs — no direct pushes to `main`
- Branch naming: `feature/<sprint-name>`
- Preserve all feature branches after merge (audit trail)

## Sprint Workflow

1. Verify the GitHub Issue exists for the sprint
2. Create and checkout the feature branch
3. Implement with TDD (backend) or behavior tests (frontend)
4. Verify all tests pass + build succeeds
5. Commit with conventional commit messages
6. Push and open a PR referencing the issue

## Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add task delete endpoint
fix: correct timezone conversion for overnight hours
test: add API tests for developer delete
docs: add setup guide
```

## Code Conventions

### Backend (Python)

- Follow existing patterns in the directory structure
- Async/await for all database operations
- Pydantic v2 for request/response schemas
- Type hints on all functions

### Frontend (TypeScript)

- TypeScript strict mode
- Components in feature folders
- App Router with route groups (`(auth)`, `(dashboard)`)
- React Query for server state
- Tailwind CSS for styling

### PR Workflow

1. All changes go through PRs
2. Squash and merge (keeps main history clean)
3. Reference the issue in the PR description
4. Present the [Manual Review Checklist](#manual-review-checklist) before merging

## Manual Review Checklist

After raising a PR, verify these before merging:

### Automated Checks

```bash
# Backend tests
python -m pytest -v
# Expect: all tests passing, 0 warnings

# Frontend tests
cd frontend && npm run test
# Expect: all tests passing

# Frontend build
cd frontend && npm run build
# Expect: clean build, no errors
```

### Manual Verification

Start the database, seed it, then start both dev servers:

```bash
docker compose up -d
python -m backend.seed
uvicorn backend.main:app --reload
cd frontend && npm run dev
```

Open [http://localhost:3000](http://localhost:3000) and verify new features.

### Code Changes

List every file changed with a one-line summary. Group by backend/frontend/tests.

### Issue Checklist

Confirm all items in the GitHub Issue checklist are checked off.

### Deferred Items

List any items explicitly deferred, or state "None."
