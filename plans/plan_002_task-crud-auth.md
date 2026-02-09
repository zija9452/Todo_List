# Implementation Plan: Full-Stack Multi-User Todo Application

**Branch**: `001-full-stack-todo` | **Date**: 2026-02-09 | **Spec**: [specs/001-full-stack-todo/spec.md](../specs/001-full-stack-todo/spec.md)
**Input**: Feature specification from `/specs/001-full-stack-todo/spec.md`

## Plan Metadata

```yaml
plan_id: 002
specs_refs: @specs/features/task-crud.md, @specs/features/authentication.md
current_phase: 2
phase_status: in_progress
scope_limit: phase_2_only
```

## Objective

Deliver a production-quality Phase II implementation featuring backend FastAPI + SQLModel, Neon Postgres persistence, Better Auth (JWT) on frontend (Next.js), secured REST API, tests, and CLAUDE trace.

## Milestones

**M1: Finalize specs & plans**
- Done when: specs exist for task-crud & authentication with all clarifications integrated

**M2: Backend skeleton + DB models + migrations + auth middleware**
- Done when: Backend models, database connection, migrations, and JWT authentication middleware are implemented

**M3: CRUD routes + unit tests**
- Done when: All required API endpoints are implemented with proper error handling and unit tests pass

**M4: Frontend auth integration + API client + task pages + smoke tests**
- Done when: Frontend integrates Better Auth, API client attaches JWT headers, and UI components allow full task management

**M5: Integration tests, CI config, CLAUDE.md trace, and docs**
- Done when: Integration tests pass, CI is configured, documentation is updated, and Phase II acceptance criteria are met

## Atomic Tasks

**T001** — Spec finalize: ensure `specs/features/task-crud.md` includes explicit CLI/API contract, data schema, and acceptance criteria. Output: spec v1.1 + commit `spec(002): finalize task-crud`.

**T002** — Spec create/update: `specs/features/authentication.md` with JWT details and ownership rules. Output: spec + commit `spec(002-auth): add auth spec`.

**T010** — Plan create: write `plans/plan_002_task-crud-auth.md` (this artifact).

**T020** — Backend: add `backend/src/models.py` (SQLModel Task model) + migrations scaffold. Tests: model schema test. Commit `feat(002-model): add Task model`.

**T030** — Backend DB: `backend/src/db.py` Neon connection + env var handling. Commit `chore(db): add Neon config`.

**T040** — Auth middleware: `backend/src/auth.py` verifies JWT (uses `pyjwt` if spec justifies). Tests: token verification & claim extraction. Commit `feat(002-auth): add JWT middleware`.

**T050** — Routes: implement CRUD endpoints with ownership enforcement. Tests: unit tests for each route (401/403/404/422 covered). Commit `feat(002-crud): implement endpoints`.

**T060** — Frontend: implement Better Auth config to request JWT and store session; `frontend/lib/api.ts` attaches `Authorization` header. Smoke tests: login + create task flow. Commit `feat(002-frontend-auth)`.

**T070** — Frontend pages/components: dashboard, new task form, task detail/edit. Tests: component + E2E smoke. Commit `feat(002-frontend-ui)`.

**T080** — Integration tests: end-to-end flows using test secret or token fixtures. Commit `test(002-integration)`.

**T090** — CI & docs: add `backend/.github/workflows/ci.yml` (pytest) and `frontend` build/test checks; update `CLAUDE.md` and `README.md`. Commit `chore(ci): add CI`.

## Decisions to Document

**ID1: ID format decision**
- Options: Sequential int (phase II) vs UUID (scalable)
- Recommended: Sequential int for simplicity
- Tradeoffs: Sequential ints are simpler to work with but less scalable; UUIDs offer global uniqueness but are harder to remember

**ID2: JWT library decision**
- Options: `pyjwt` vs `authlib` vs custom
- Recommended: `pyjwt` for its widespread adoption and simple API
- Tradeoffs: `pyjwt` is well-documented but `authlib` offers more built-in OAuth features; custom solution would require more maintenance

**ID3: Migrations approach**
- Options: Use Alembic vs SQLModel built-in approach
- Recommended: Alembic for its robust migration handling
- Tradeoffs: Alembic is more complex to set up but handles complex schema changes better than built-in approach

**ID4: Test strategy decision**
- Options: Mock JWT vs real token signed with test secret in integration tests
- Recommended: Test secret to exercise real verification
- Tradeoffs: Real tokens test the full authentication flow but require more setup; mocks are simpler but may miss integration issues

**ID5: Frontend auth flow decision**
- Options: Different approaches for storing and using JWT in Next.js
- Recommended: Better Auth session management with secure storage
- Tradeoffs: Direct JWT storage is more flexible but sessions provide better security practices

## Testing & QA Strategy

**Unit tests**: For each backend handler and middleware (pytest)
- Test individual API endpoints in isolation
- Verify authentication middleware behavior
- Validate data model operations

**Integration tests**: Create user token (signed with test `BETTER_AUTH_SECRET`), create task, list tasks, update, delete; assert ownership enforcement
- Full end-to-end testing of the authentication and task management flow
- Verify that ownership rules are properly enforced
- Test error conditions and boundary cases

**Frontend smoke tests**: Login -> create -> list -> toggle -> delete (Playwright or RTL)
- Verify the complete user journey works as expected
- Test UI interactions and state management
- Validate proper JWT attachment to API calls

**CI**: Failing tests fail pipeline; add commands in README for local test runs
- Automated testing of all functionality
- Quality gates to prevent broken builds

## Dev/Run Commands and Environment Variables

**Environment variables (.env.example)**:
```
BETTER_AUTH_SECRET=changeme
DATABASE_URL=postgresql://user:pass@host:5432/db
NEXT_PUBLIC_AUTH_ORIGIN=http://localhost:3000
```

**Backend dev run**: `cd backend && uvicorn src.main:app --reload --port 8000`

**Frontend dev**: `cd frontend && npm run dev`

**Tests**:
- `cd backend && python -m pytest`
- `cd frontend && npm test` (or `npm run test`)

## Acceptance Checklist

- [ ] All endpoints implemented and return 200/201 or proper error codes per contract
- [ ] Backend rejects requests missing/invalid JWT with 401
- [ ] Ownership enforced: a user cannot access another user's tasks (403)
- [ ] Tasks persist in Neon (manual or CI-run reboot test shows data persists)
- [ ] Unit + integration tests pass
- [ ] CLAUDE.md updated with spec→plan→artifact trace
- [ ] `current_phase: 2` and `phase_status: in_progress` metadata remain until acceptance is declared

## Next Action for Claude Code Agent

Produce `plans/plan_002_task-crud-auth.md` in `/plans/` with the full structure above and the atomic tasks listed (T001..T090). Then create or update `specs/features/authentication.md` header snippet with required Gherkin AC. Commit both with messages `chore(plan): add plan_002_task-crud-auth` and `spec(002-auth): add authentication spec header`.