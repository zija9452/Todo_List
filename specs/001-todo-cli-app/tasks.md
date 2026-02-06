# Tasks: Evolution of Todo CLI App

**Feature**: 001-todo-cli-app
**Created**: 2026-02-02
**Status**: Planned

## Implementation Strategy

MVP approach focusing on delivering a complete, independently testable feature with each user story. Begin with User Story 1 (foundational functionality) and incrementally add complexity.

## Phase 1: Setup & Project Initialization

- [x] T001 Create project structure with src/ and tests/ directories per implementation plan
- [x] T002 Initialize Python project with pyproject.toml including pytest dependency
- [x] T003 [P] Create basic directory structure following single-file architecture

## Phase 2: Foundational Components

- [x] T010 Implement Task data model in src/todo_app.py with all required attributes
- [x] T011 Implement TodoList class with in-memory storage in src/todo_app.py
- [x] T012 Create CLI argument parser using argparse in src/todo_app.py
- [x] T013 Create basic test structure in tests/test_todo_app.py

## Phase 3: User Story 1 - Add and List Tasks (Priority: P1)

**Story Goal**: User can create and view a list of tasks using command-line interface

**Independent Test**: Can be fully tested by adding tasks via the `todo add` command and listing them with `todo list`, delivering the core value of maintaining a todo list

**Acceptance Scenarios**:
1. **Given** user opens CLI, **When** user runs `todo add "Complete project proposal"`, **Then** task appears in the task list with a sequential ID
2. **Given** user has added multiple tasks, **When** user runs `todo list`, **Then** all tasks are displayed with their IDs and completion status

- [x] T020 [P] [US1] Implement Task model with ID, description, completion status, priority, due date, creation timestamp
- [x] T021 [P] [US1] Implement TodoList class with add_task and get_tasks methods
- [x] T022 [US1] Implement CLI add command handler in src/todo_app.py
- [x] T023 [US1] Implement CLI list command handler with default sort (creation time ascending)
- [x] T024 [P] [US1] Create unit tests for add functionality in tests/test_todo_app.py
- [x] T025 [P] [US1] Create unit tests for list functionality in tests/test_todo_app.py

## Phase 4: User Story 2 - Update and Delete Tasks (Priority: P2)

**Story Goal**: User can modify or remove existing tasks from their todo list

**Independent Test**: Can be fully tested by creating tasks, updating them with `todo update`, and deleting them with `todo delete`, delivering flexibility in task management

**Acceptance Scenarios**:
1. **Given** user has existing task with ID 1, **When** user runs `todo update 1 "Revise project proposal"`, **Then** task description is updated while keeping the same ID
2. **Given** user has existing task with ID 2, **When** user runs `todo delete 2`, **Then** task is removed from the list and no longer appears in listings

- [x] T030 [P] [US2] Implement update_task method in TodoList class
- [x] T031 [P] [US2] Implement delete_task method in TodoList class
- [x] T032 [US2] Implement CLI update command handler in src/todo_app.py
- [x] T033 [US2] Implement CLI delete command handler in src/todo_app.py
- [x] T034 [P] [US2] Create unit tests for update functionality in tests/test_todo_app.py
- [x] T035 [P] [US2] Create unit tests for delete functionality in tests/test_todo_app.py

## Phase 5: User Story 3 - Toggle Task Completion (Priority: P3)

**Story Goal**: User can mark tasks as completed when they finish them, or unmark them if they need to revisit them

**Independent Test**: Can be fully tested by toggling task completion with `todo toggle`, delivering the ability to track task status

**Acceptance Scenarios**:
1. **Given** user has pending task with ID 1, **When** user runs `todo toggle 1`, **Then** task status changes to completed and displays with a completed indicator
2. **Given** user has completed task with ID 1, **When** user runs `todo toggle 1`, **Then** task status changes back to pending

- [x] T040 [P] [US3] Implement toggle_complete method in TodoList class
- [x] T041 [US3] Implement CLI toggle command handler in src/todo_app.py
- [x] T042 [P] [US3] Create unit tests for toggle functionality in tests/test_todo_app.py

## Phase 6: User Story 4 - Sort Task Lists (Priority: P4)

**Story Goal**: User can view their tasks organized in a specific order (by title, priority, due date, or creation date) in either ascending or descending order

**Independent Test**: Can be fully tested by adding multiple tasks and sorting them with `todo list --sort {title,priority,due,created} --order {asc,desc}`, delivering organized task presentation

**Acceptance Scenarios**:
1. **Given** user has multiple tasks, **When** user runs `todo list --sort title --order asc`, **Then** tasks are displayed alphabetically by title in ascending order
2. **Given** user has tasks with due dates (some null), **When** user runs `todo list --sort due --order asc`, **Then** tasks with due dates appear first in chronological order, then tasks with no due dates

- [x] T050 [P] [US4] Implement sort_tasks method in TodoList class with all required sort options
- [x] T051 [US4] Enhance CLI list command with --sort and --order options
- [x] T052 [P] [US4] Create unit tests for sort functionality in tests/test_todo_app.py
- [x] T053 [P] [US4] Test edge cases: missing due dates sorting last for asc, stable sorting for ties

## Phase 7: Polish & Cross-Cutting Concerns

- [x] T060 Implement error handling for invalid task IDs (display message but continue execution)
- [x] T061 Add input validation for due date format (ISO 8601 YYYY-MM-DD)
- [x] T062 Implement priority validation (integer values 1-3)
- [x] T063 Add CLI help text and usage information + interactive mode
- [x] T064 Run full test suite and fix any failing tests
- [x] T065 Update README.md with setup and usage instructions
- [x] T066 Create CLAUDE.md with agent transcripts and implementation details
- [x] T067 Final verification that all functional requirements are met (FR-001 through FR-015)

## Dependencies

- User Story 1 must be completed before User Story 2 (Update/Delete depend on Add/List existing)
- User Story 2 should be completed before User Story 3 (Toggle requires task management foundation)
- User Story 3 should be completed before User Story 4 (Sort operates on existing functionality)

## Parallel Execution Opportunities

- [US1] Tasks T020 and T021 can run in parallel (Task model and TodoList class)
- [US1] Tasks T024 and T025 can run in parallel (Add and List tests)
- [US2] Tasks T030 and T031 can run in parallel (Update and Delete methods)
- [US2] Tasks T034 and T035 can run in parallel (Update and Delete tests)
- [US4] Tasks T052 and T053 can run in parallel (Sort tests and edge cases)

## MVP Scope

Minimum Viable Product includes User Story 1: Add and List Tasks functionality with basic CLI interface and tests.