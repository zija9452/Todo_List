---
id: 3
title: Create implementation plan
stage: plan
date: 2026-02-09
surface: agent
model: Claude Haiku 4.5
feature: 001-full-stack-todo
branch: 001-full-stack-todo
user: user
command: /sp.plan
labels: ["plan", "full-stack", "todo-app", "api", "authentication"]
links:
  spec: specs/001-full-stack-todo/spec.md
  plan: plans/plan_002_task-crud-auth.md
  ticket: null
  adr: null
  pr: null
files:
  - "plans/plan_002_task-crud-auth.md"
  - "specs/features/authentication.md"
tests: []
---

## Prompt

/sp.plan
"""
Project: Evolution of Todo — Phase II (Full-Stack Web) — Claude Code Plan Prompt

Context for Claude Code:
You are implementing **Phase II only**. Read `/CLAUDE.md`, `/specs/features/task-crud.md`, and `/specs/features/authentication.md` before doing anything. All work must be spec-driven: create/update specs first, then a plan, then generate code/tests/docs. Do not begin Phase III+.

Goal (high level)

* Deliver a production-quality Phase II implementation plan that agents can execute: backend FastAPI + SQLModel, Neon Postgres persistence, Better Auth (JWT) on frontend (Next.js), secured REST API, tests, and CLAUDE trace.

Primary outputs for this prompt (produce these artifacts immediately):

1. `plans/plan_002_task-crud-auth.md` — full plan for task CRUD + authentication (outline tasks, files, tests, order, and acceptance checks).
2. If missing, update: `/specs/features/authentication.md` (short header snippet + Gherkin acceptance criteria).
3. A 1-page architecture sketch (textual diagram + responsibilities).
4. A prioritized task list (atomic subtasks) with estimated relative effort (S/M/L).

Plan structure (the plan file must contain these sections)

* Title & metadata:

  * `plan_id: 002`
  * `specs_refs: @specs/features/task-crud.md, @specs/features/authentication.md`
  * `current_phase: 2`
  * `phase_status: in_progress`
  * `scope_limit: phase_2_only`
* Objective: one-sentence objective.
* Milestones (M1..Mn) with clear done-conditions.
* Atomic tasks (T001..T0xx) with: action, target files, outputs, tests, commit message pattern.
* Decisions to document (each with options + recommended choice + tradeoffs).
* Testing & QA strategy (unit/integration/smoke/CI).
* Dev/Run commands and environment variables.
* Acceptance checklist (what to verify to mark Phase II accepted).
* Next-action for Claude Code agent (the first task to run now).

Concrete Milestones (must appear)

* M1: Finalize specs & plans (specs exist for task-crud & authentication).
* M2: Backend skeleton + DB models + migrations + auth middleware.
* M3: CRUD routes + unit tests.
* M4: Frontend auth integration + API client + task pages + smoke tests.
* M5: Integration tests, CI config, CLAUDE.md trace, and docs.

Example Atomic Tasks (must be included; ensure at least these)

* T001 — Spec finalize: ensure `specs/features/task-crud.md` includes explicit CLI/API contract, data schema, and acceptance criteria. Output: spec v1.1 + commit `spec(002): finalize task-crud`.
* T002 — Spec create/update: `specs/features/authentication.md` with JWT details and ownership rules. Output: spec + commit `spec(002-auth): add auth spec`.
* T010 — Plan create: write `plans/plan_002_task-crud-auth.md` (this artifact).
* T020 — Backend: add `backend/src/models.py` (SQLModel Task model) + migrations scaffold. Tests: model schema test. Commit `feat(002-model): add Task model`.
* T030 — Backend DB: `backend/src/db.py` Neon connection + env var handling. Commit `chore(db): add Neon config`.
* T040 — Auth middleware: `backend/src/auth.py` verifies JWT (uses `pyjwt` if spec justifies). Tests: token verification & claim extraction. Commit `feat(002-auth): add JWT middleware`.
* T050 — Routes: implement CRUD endpoints with ownership enforcement. Tests: unit tests for each route (401/403/404/422 covered). Commit `feat(002-crud): implement endpoints`.
* T060 — Frontend: implement Better Auth config to request JWT and store session; `frontend/lib/api.ts` attaches `Authorization` header. Smoke tests: login + create task flow. Commit `feat(002-frontend-auth)`.
* T070 — Frontend pages/components: dashboard, new task form, task detail/edit. Tests: component + E2E smoke. Commit `feat(002-frontend-ui)`.
* T080 — Integration tests: end-to-end flows using test secret or token fixtures. Commit `test(002-integration)`.
* T090 — CI & docs: add `backend/.github/workflows/ci.yml` (pytest) and `frontend` build/test checks; update `CLAUDE.md` and `README.md`. Commit `chore(ci): add CI`.

Decisions to document (must be recorded in plan)

* ID format: sequential int (phase II) vs UUID (scalable). Recommend sequential int for simplicity; record tradeoffs.
* JWT library: `pyjwt` vs `authlib` vs custom. If using `pyjwt`, add spec justification and `pyproject.toml` change.
* Migrations: use Alembic or SQLModel built-in approach. Recommend Alembic if schema will change later.
* Test strategy: mock JWT vs real token signed with test secret in integration tests. Recommend test secret to exercise real verification.
* Frontend auth flow: Better Auth session -> JWT accessible in client? Document secure storage and refresh handling.

Testing & QA (must be explicit)

* Unit tests for each backend handler and middleware (pytest).
* Integration tests: create user token (signed with test `BETTER_AUTH_SECRET`), create task, list tasks, update, delete; assert ownership enforcement.
* Frontend smoke tests: login -> create -> list -> toggle -> delete (Playwright or RTL).
* CI: failing tests fail pipeline; add commands in README for local test runs.

Environment & run commands (include exact variable names)

* `.env.example` must include:

  * `BETTER_AUTH_SECRET=changeme`
  * `DATABASE_URL=postgresql://user:pass@host:5432/db`
  * `NEXT_PUBLIC_AUTH_ORIGIN=http://localhost:3000`
* Backend dev run: `cd backend && uvicorn src.main:app --reload --port 8000`
* Frontend dev: `cd frontend && npm run dev`
* Tests: `cd backend && python -m pytest`, `cd frontend && npm test` (or `npm run test`)

Acceptance checklist (agent must verify)

* All endpoints implemented and return 200/201 or proper error codes per contract.
* Backend rejects requests missing/invalid JWT with 401.
* Ownership enforced: a user cannot access another user's tasks (403).
* Tasks persist in Neon (manual or CI-run reboot test shows data persists).
* Unit + integration tests pass.
* CLAUDE.md updated with spec→plan→artifact trace.
* `current_phase: 2` and `phase_status: in_progress` metadata remain until acceptance is declared.

First action (what Claude Code should do now)

* Produce `plans/plan_002_task-crud-auth.md` in `/plans/` with the full structure above and the atomic tasks listed (T001..T090). Then create or update `specs/features/authentication.md` header snippet with required Gherkin AC. Commit both with messages `chore(plan): add plan_002_task-crud-auth` and `spec(002-auth): add authentication spec header`.

Constraints & governance reminders (must be repeated in plan)

* **Spec-first**; do not write production code before specs + plan exist.
* **No secrets in repo**; `.env.example` only.
* **All code must be generated by Claude Code**; human edits limited to docs unless spec allows.
* Phase lock: **do not** start Phase III until Phase II acceptance conditions are met.

Deliverable format

* Return the `plans/plan_002_task-crud-auth.md` content in Markdown (include metadata block).
* Also return the `specs/features/authentication.md` header snippet (3–6 lines) in Markdown.

Do not ask follow-up questions — create the plan and spec header now and commit them as the immediate next artifacts.
"""

## Response snapshot

Successfully created the implementation plan for the Full-Stack Multi-User Todo Application. Two key artifacts were produced:

1. `plans/plan_002_task-crud-auth.md` - A comprehensive implementation plan with:
   - Plan metadata with required fields (plan_id, specs_refs, current_phase, etc.)
   - Clear objective for Phase II implementation
   - Five detailed milestones (M1-M5) with done-conditions
   - Ten atomic tasks (T001-T090) covering the entire implementation
   - Five key architectural decisions documented with tradeoffs
   - Complete testing and QA strategy
   - Environment variables and run commands
   - Acceptance checklist with verification steps
   - Next action guidance

2. `specs/features/authentication.md` - An authentication feature specification with:
   - Clear feature title and description
   - Three Gherkin acceptance criteria scenarios covering auth flow, unauthorized access, and unauthenticated access

Both artifacts are ready for the next phase of implementation.

## Outcome

- ✅ Impact: Created comprehensive plan and auth spec for Phase II implementation
- 🧪 Tests: No tests required for plan creation
- 📁 Files: plans/plan_002_task-crud-auth.md and specs/features/authentication.md created
- 🔁 Next prompts: Ready for task generation with /sp.tasks
- 🧠 Reflection: Plan covers all requirements from user prompt with clear milestones

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - all required artifacts created
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to /sp.tasks for task breakdown