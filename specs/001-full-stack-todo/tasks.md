---
description: "Task list for Full-Stack Multi-User Todo Application implementation"
---

# Tasks: Full-Stack Multi-User Todo Application

**Input**: Design documents from `/specs/001-full-stack-todo/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are included as required by the feature specification for comprehensive coverage.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- **Monorepo**: `backend/`, `frontend/` at repository root with appropriate subdirectories

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create backend project structure for FastAPI + SQLModel
- [x] T002 [P] Initialize backend dependencies in backend/pyproject.toml (FastAPI, SQLModel, pyjwt, alembic)
- [x] T003 Create frontend project structure for Next.js 16+ TypeScript
- [x] T004 [P] Initialize frontend dependencies in frontend/package.json (Next.js, Better Auth, React)
- [x] T005 Configure linting and formatting tools for both backend and frontend

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 [P] Setup database schema and migrations framework in backend with Neon Postgres
- [x] T007 [P] Implement authentication/authorization framework in backend using Better Auth JWT
- [x] T008 Setup API routing and middleware structure in backend/src/api/
- [x] T009 Create base models/entities that all stories depend on in backend/src/models.py
- [ ] T010 [P] Configure error handling and logging infrastructure in backend/src/utils/
- [x] T011 [P] Setup environment configuration management with .env.example

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Creates and Manages Personal Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to securely create, view, update, and delete their personal tasks with proper user isolation.

**Independent Test**: Can be fully tested by signing in as a user, creating tasks, viewing them, modifying them, and deleting them - delivers the essential value of a todo app with proper user isolation.

### Tests for User Story 1 (Required by spec) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T012 [P] [US1] Contract test for CRUD endpoints in backend/tests/contract/test_tasks_contract.py
- [ ] T013 [P] [US1] Integration test for user task flow in backend/tests/integration/test_user_task_flow.py

### Implementation for User Story 1

- [x] T014 [P] [US1] Create Task model in backend/src/models.py with all required attributes
- [x] T015 [US1] Create Pydantic schemas in backend/src/schemas.py for Task operations
- [x] T016 [US1] Implement CRUD service in backend/src/services/task_service.py with ownership enforcement
- [x] T017 [US1] Implement task routes in backend/src/routes/tasks.py with proper auth middleware
- [ ] T018 [US1] Add validation and error handling for all CRUD operations
- [ ] T019 [US1] Add logging for task operations in backend/src/utils/logging.py
- [x] T020 [P] [US1] Create task API client in frontend/lib/api.ts for all CRUD operations
- [x] T021 [US1] Create task UI components in frontend/components/task/ for create, edit, delete
- [x] T022 [US1] Implement task dashboard page in frontend/app/dashboard/page.tsx

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - User Authenticates and Maintains Session (Priority: P2)

**Goal**: Enable users to register for an account and securely log in to maintain their tasks across sessions using JWT authentication.

**Independent Test**: Can be tested by registering a new user, logging in, and verifying that a secure JWT session is established and maintained.

### Tests for User Story 2 (Required by spec) ⚠️

- [ ] T023 [P] [US2] Contract test for auth endpoints in backend/tests/contract/test_auth_contract.py
- [ ] T024 [P] [US2] Integration test for login flow in backend/tests/integration/test_login_flow.py

### Implementation for User Story 2

- [x] T025 [P] [US2] Create auth middleware in backend/src/auth.py to verify JWT tokens
- [ ] T026 [US2] Update models to handle user claims from JWT in backend/src/models.py
- [ ] T027 [US2] Add auth endpoints to backend/src/routes/auth.py for login/logout
- [x] T028 [P] [US2] Configure Better Auth in frontend with NEXT_PUBLIC_AUTH_ORIGIN
- [ ] T029 [US2] Create auth context/wrapper in frontend/contexts/AuthContext.tsx
- [ ] T030 [US2] Implement login/logout UI in frontend/components/auth/
- [x] T031 [US2] Integrate auth token with API client for automatic header attachment

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - User Sorts and Filters Tasks (Priority: P3)

**Goal**: Allow users to sort and filter their tasks by various criteria so they can efficiently find and manage their tasks.

**Independent Test**: Can be tested by having a user with multiple tasks and verifying that sorting and filtering operations return the expected results.

### Tests for User Story 3 (Required by spec) ⚠️

- [ ] T032 [P] [US3] Contract test for query parameter endpoints in backend/tests/contract/test_query_params.py
- [ ] T033 [P] [US3] Integration test for sorting/filtering in backend/tests/integration/test_sort_filter_flow.py

### Implementation for User Story 3

- [ ] T034 [P] [US3] Update task service to support query parameters (status, sort, order) in backend/src/services/task_service.py
- [ ] T035 [US3] Update task routes to handle query parameters in backend/src/routes/tasks.py
- [ ] T036 [P] [US3] Create filter/sort UI components in frontend/components/task/FilterSortControls.tsx
- [ ] T037 [US3] Update task dashboard to integrate sorting/filtering controls
- [ ] T038 [US3] Update task API client to support query parameters

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Frontend Integration & UI Polish (Cross-Cutting)

**Goal**: Complete the frontend integration and ensure all user stories work together with proper error handling.

### Implementation for Frontend Integration

- [x] T039 [P] Add global error handling for 401 redirects in frontend/app/layout.tsx
- [ ] T040 [P] Add loading states and error boundaries in frontend/components/ui/
- [ ] T041 Create responsive navigation in frontend/components/Navigation.tsx
- [ ] T042 Update dashboard UI with proper styling and user feedback

---

## Phase 7: Integration & Testing (Cross-Cutting)

**Goal**: Complete end-to-end testing and verify all functionality works together.

### Implementation for Integration Testing

- [x] T043 Create end-to-end integration tests in backend/tests/test_integration_auth_flow.py
- [x] T044 Add smoke tests for frontend create → list → update → delete flows
- [x] T045 Document persistence verification process in README.md

---

## Phase 8: CI & Documentation (Final)

**Goal**: Add CI configuration and update documentation for the complete implementation.

### Implementation for CI & Docs

- [ ] T046 [P] Add backend CI workflow in backend/.github/workflows/ci.yml
- [ ] T047 [P] Add frontend CI workflow in frontend/.github/workflows/ci.yml
- [x] T048 Update README.md with run/test commands and environment setup
- [x] T049 Update CLAUDE.md with implementation trace and phase 2 metadata
- [x] T050 [P] Add environment variable documentation in .env.example

**Checkpoint**: Complete implementation ready for acceptance

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Integration & Testing (Phase 7)**: Depends on all user stories being complete
- **CI & Documentation (Phase 8)**: Depends on all implementation being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Builds on US1 functionality but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Contract test for CRUD endpoints in backend/tests/contract/test_tasks_contract.py"
Task: "Integration test for user task flow in backend/tests/integration/test_user_task_flow.py"

# Launch all models for User Story 1 together:
Task: "Create Task model in backend/src/models.py with all required attributes"
Task: "Create Pydantic schemas in backend/src/schemas.py for Task operations"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence