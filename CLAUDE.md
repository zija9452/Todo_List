# Claude Code Instructions for Full-Stack Todo Application

## Project Overview

This project implements a multi-user full-stack todo application with:
- Backend: FastAPI + SQLModel, Neon Postgres persistence, JWT verification middleware
- Frontend: Next.js 16+ (App Router, TypeScript), Better Auth integration
- Secured REST API with ownership enforcement

## Phase Status
- **Current Phase**: 2
- **Phase Status**: in_progress
- **Scope Limit**: phase_2_only

## Project Structure
```
backend/
├── src/
│   ├── models.py          # SQLModel Task model
│   ├── db.py              # Database connection and session management
│   ├── auth.py            # JWT authentication middleware
│   ├── schemas.py         # Pydantic request/response schemas
│   ├── services/
│   │   └── task_service.py # Task business logic
│   ├── routes/
│   │   └── tasks.py       # API routes for task operations
│   └── main.py            # Main FastAPI application
├── pyproject.toml         # Backend dependencies
└── tests/                 # Backend tests

frontend/
├── app/                   # Next.js App Router pages
│   ├── layout.tsx         # Root layout with navigation
│   ├── dashboard/page.tsx # Task dashboard
│   ├── tasks/
│   │   ├── new/page.tsx   # Create new task page
│   │   └── [id]/page.tsx  # Task detail/edit page
├── lib/
│   ├── api.ts             # API client with JWT handling
│   └── auth.ts            # Auth utilities
├── package.json           # Frontend dependencies
└── globals.css            # Global styles

Root/
├── .env.example           # Environment variables template
├── README.md              # Project documentation
└── CLAUDE.md              # This file
```

## Implementation Trace

### Prompt → Plan → Generated Files → Test Outputs

#### Phase 1: Setup (Shared Infrastructure)
- **Prompt**: Create backend project structure for FastAPI + SQLModel
- **Plan**: T001 - Create backend project structure
- **Generated Files**: backend/src/, backend/pyproject.toml
- **Tests**: N/A

- **Prompt**: Initialize backend dependencies in backend/pyproject.toml
- **Plan**: T002 - Initialize backend dependencies (FastAPI, SQLModel, pyjwt, alembic)
- **Generated Files**: backend/pyproject.toml
- **Tests**: N/A

- **Prompt**: Create frontend project structure for Next.js 16+ TypeScript
- **Plan**: T003 - Create frontend project structure
- **Generated Files**: frontend/, frontend/package.json
- **Tests**: N/A

#### Phase 2: Foundational (Blocking Prerequisites)
- **Prompt**: Create base models/entities that all stories depend on in backend/src/models.py
- **Plan**: T009 - Create Task model in backend/src/models.py with all required attributes
- **Generated Files**: backend/src/models.py
- **Tests**: N/A

- **Prompt**: Create DB connection in backend/src/db.py
- **Plan**: T011 - Setup DB connection via DATABASE_URL
- **Generated Files**: backend/src/db.py
- **Tests**: N/A

- **Prompt**: Create auth middleware in backend/src/auth.py
- **Plan**: T025 - Create auth middleware to verify JWT tokens
- **Generated Files**: backend/src/auth.py
- **Tests**: N/A

#### Phase 3: User Story 1 - User Creates and Manages Personal Tasks (Priority: P1)
- **Prompt**: Create Pydantic schemas in backend/src/schemas.py for Task operations
- **Plan**: T015 - Create Pydantic schemas for Task operations
- **Generated Files**: backend/src/schemas.py
- **Tests**: N/A

- **Prompt**: Implement CRUD service in backend/src/services/task_service.py with ownership enforcement
- **Plan**: T016 - Implement CRUD service with ownership enforcement
- **Generated Files**: backend/src/services/task_service.py
- **Tests**: N/A

- **Prompt**: Implement task routes in backend/src/routes/tasks.py with proper auth middleware
- **Plan**: T017 - Implement task routes with proper auth middleware
- **Generated Files**: backend/src/routes/tasks.py
- **Tests**: N/A

- **Prompt**: Create task API client in frontend/lib/api.ts for all CRUD operations
- **Plan**: T020 - Create task API client in frontend/lib/api.ts
- **Generated Files**: frontend/lib/api.ts
- **Tests**: N/A

- **Prompt**: Create task UI components in frontend/components/task/ for create, edit, delete
- **Plan**: T021 - Create task UI components for create, edit, delete
- **Generated Files**: frontend/app/tasks/new/page.tsx, frontend/app/tasks/[id]/page.tsx
- **Tests**: N/A

- **Prompt**: Implement task dashboard page in frontend/app/dashboard/page.tsx
- **Plan**: T022 - Implement task dashboard page
- **Generated Files**: frontend/app/dashboard/page.tsx
- **Tests**: N/A

#### Phase 6: Frontend Integration & UI Polish
- **Prompt**: Add global error handling for 401 redirects in frontend/app/layout.tsx
- **Plan**: T039 - Add global error handling for 401 redirects
- **Generated Files**: frontend/app/layout.tsx
- **Tests**: N/A

#### Phase 8: CI & Documentation (Final)
- **Prompt**: Update README.md with run/test commands and environment setup
- **Plan**: T048 - Update README.md with run/test commands and environment setup
- **Generated Files**: README.md
- **Tests**: N/A

- **Prompt**: Update CLAUDE.md with implementation trace and phase 2 metadata
- **Plan**: T049 - Update CLAUDE.md with implementation trace
- **Generated Files**: CLAUDE.md
- **Tests**: N/A

## Environment Variables
- `BETTER_AUTH_SECRET` - Secret for JWT token signing/verification
- `DATABASE_URL` - Connection string for Neon Postgres database
- `NEXT_PUBLIC_AUTH_ORIGIN` - Origin for Better Auth configuration

## Next Steps
- Complete integration tests for backend
- Add frontend smoke tests
- Set up CI workflows
- Run persistence verification tests

## Architecture Notes
- Backend uses FastAPI with SQLModel for database operations
- Authentication is handled via JWT tokens with Better Auth
- Frontend uses Next.js App Router for page structure
- All API calls include Authorization header with JWT token
- User ownership is enforced at the API level