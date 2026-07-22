# Architectural Decisions

## 1. Async SQLAlchemy + asyncpg

**Decision:** Use async SQLAlchemy with asyncpg driver.

**Why:** FastAPI is async-native. Blocking DB calls would bottleneck the event loop. Asyncpg is the fastest Python PostgreSQL driver.

**Alternatives considered:** Sync SQLAlchemy (rejected — would block the event loop), databases library (rejected — less mature ORM integration).

## 2. Repository + Service Pattern

**Decision:** Separate repositories (DB queries) from services (business logic).

**Why:** Testability — services can be tested with mock repositories. Clear separation of concerns. Repositories handle SQL, services handle rules.

**Structure:**
- `repositories/` — Thin layer over SQLAlchemy queries
- `services/` — Business logic, calls repositories

## 3. Pydantic v2 Schemas

**Decision:** Pydantic v2 for all request/response validation.

**Why:** Native SQLAlchemy 2.0 integration, fast validation (Rust core), auto-generated OpenAPI docs. Single source of truth for API contracts.

## 4. JWT with HTTPBearer

**Decision:** Use `HTTPBearer` scheme instead of OAuth2 password flow in Swagger.

**Why:** Simpler for SPA clients. Token goes in `Authorization: Bearer <token>` header directly. Works cleanly with Swagger's "Authorize" button.

## 5. SQLite for Tests, PostgreSQL for Dev/Prod

**Decision:** Tests use `aiosqlite` in-memory DB. Dev uses Docker PostgreSQL.

**Why:** Tests run fast without Docker dependency. Production parity maintained in dev environment. CI stays lightweight.

## 6. Direct Browser-to-Backend API Calls

**Decision:** Frontend calls Railway backend directly via `NEXT_PUBLIC_API_URL`, not through a Vercel proxy.

**Why:** Vercel's Next.js rewrite proxy returned `DNS_HOSTNAME_RESOLVED_PRIVATE` when forwarding to Railway. Direct browser calls bypass this issue entirely. The centralized `apiFetch` function in `api.ts` prepends the base URL to all requests, making the architecture transparent to the rest of the codebase.

**Development fallback:** When `NEXT_PUBLIC_API_URL` is unset, requests default to `http://localhost:8000` for local development.

## 7. Shared Label Constants

**Decision:** `lib/labels.ts` exports status/priority labels used across all pages.

**Why:** Eliminates duplication. Single source of truth for display text. Consistent capitalization across the app.

## 8. Role-Based Route Protection

**Decision:** FastAPI `require_role()` dependency for RBAC.

**Why:** Declarative — each route declares its required roles. Easy to audit permissions. Simple to test.

```python
@router.delete("/{task_id}", dependencies=[Depends(require_role(["admin", "manager"]))])
async def delete_task(...): ...
```

## 9. Alembic for Migrations

**Decision:** Alembic with async support for schema migrations.

**Why:** Industry standard for SQLAlchemy. Supports autogenerate from models. Works with async engines.

## 10. Idempotent Seed Script

**Decision:** Seed script checks for existing data before inserting.

**Why:** Safe to run multiple times. No duplicate data. Works in dev and CI environments.
