# Feature Specification: Evolution of Todo — Phase I (In-Memory Python CLI)

**Feature Branch**: `001-todo-cli-app`
**Created**: 2026-02-06
**Status**: Draft
**Input**: User description: "Evolution of Todo — Phase I (In-Memory Python CLI)

Target audience: Claude Code agents & student dev teams using Spec-Kit Plus.
Focus: Build an in-memory CLI todo app (Add, Delete, Update, View, Toggle Complete, Sort) via spec-driven Agentic Dev Stack — **no manual coding**.
Success criteria: All 5 features + sort implemented; unit tests pass; repo contains `CONSTITUTION.md`, `specs_history/`, `src/`, `tests/`, `README.md`, `CLAUDE.md`; each feature has a spec and passing tests.
Constraints: Python 3.13+, stdlib only (unless a spec justifies otherwise), in-memory only, spec-first workflow, sequential integer IDs preferred, stable deterministic sorting, WSL2 instructions for Windows.
CLI contract: `todo add|list|update|delete|toggle` with `--sort {title,priority,due,created}` and `--order {asc,desc}`; missing due dates sort last for asc.
Spec requirements: One spec file per feature in `specs_history/` (Gherkin-style AC), plus `plan_{spec_id}.md` and generated tests.
Commits: atomic, include sp"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add and List Tasks (Priority: P1)

A user wants to create and view a list of tasks using a command-line interface. The user should be able to add tasks to their todo list and view all tasks they have added.

**Why this priority**: This is the foundational functionality that enables all other features. Without the ability to add and view tasks, no other functionality has value.

**Independent Test**: Can be fully tested by adding tasks via the `todo add` command and listing them with `todo list`, delivering the core value of maintaining a todo list.

**Acceptance Scenarios**:

1. **Given** user opens CLI, **When** user runs `todo add "Complete project proposal"`, **Then** task appears in the task list with a sequential ID
2. **Given** user has added multiple tasks, **When** user runs `todo list`, **Then** all tasks are displayed with their IDs and completion status

---

### User Story 2 - Update and Delete Tasks (Priority: P2)

A user needs to modify or remove existing tasks from their todo list. This includes updating the task description or removing tasks that are no longer needed.

**Why this priority**: These operations provide essential lifecycle management for tasks, allowing users to maintain an accurate todo list over time.

**Independent Test**: Can be fully tested by creating tasks, updating them with `todo update`, and deleting them with `todo delete`, delivering flexibility in task management.

**Acceptance Scenarios**:

1. **Given** user has existing task with ID 1, **When** user runs `todo update 1 "Revise project proposal"`, **Then** task description is updated while keeping the same ID
2. **Given** user has existing task with ID 2, **When** user runs `todo delete 2`, **Then** task is removed from the list and no longer appears in listings

---

### User Story 3 - Toggle Task Completion (Priority: P3)

A user wants to mark tasks as completed when they finish them, or unmark them if they need to revisit them, allowing for better task tracking.

**Why this priority**: This feature allows users to track their progress and distinguish between completed and pending tasks, which is essential for productivity.

**Independent Test**: Can be fully tested by toggling task completion with `todo toggle`, delivering the ability to track task status.

**Acceptance Scenarios**:

1. **Given** user has pending task with ID 1, **When** user runs `todo toggle 1`, **Then** task status changes to completed and displays with a completed indicator
2. **Given** user has completed task with ID 1, **When** user runs `todo toggle 1`, **Then** task status changes back to pending

---

### User Story 4 - Sort Task Lists (Priority: P4)

A user wants to view their tasks organized in a specific order (by title, priority, due date, or creation date) in either ascending or descending order to improve organization.

**Why this priority**: Sorting helps users find and manage their tasks more efficiently, especially when they have many tasks.

**Independent Test**: Can be fully tested by adding multiple tasks and sorting them with `todo list --sort {title,priority,due,created} --order {asc,desc}`, delivering organized task presentation.

**Acceptance Scenarios**:

1. **Given** user has multiple tasks, **When** user runs `todo list --sort title --order asc`, **Then** tasks are displayed alphabetically by title in ascending order
2. **Given** user has tasks with due dates (some null), **When** user runs `todo list --sort due --order asc`, **Then** tasks with due dates appear first in chronological order, then tasks with no due dates

---

### Edge Cases

- How does the system handle invalid task IDs (display message but continue execution)?
- How does the system handle empty task descriptions or very long task descriptions?
- What happens when there are no tasks to list?
- How does the system handle sorting when there are mixed data types for sort fields?
- How does the system handle invalid due date formats?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to add tasks via `todo add "task description"` command
- **FR-002**: System MUST display all tasks via `todo list` command with IDs and completion status (default sort: by creation time ascending)
- **FR-003**: System MUST allow users to update task descriptions via `todo update [id] "new description"` command
- **FR-004**: System MUST allow users to delete tasks via `todo delete [id]` command
- **FR-005**: System MUST allow users to toggle task completion status via `todo toggle [id]` command
- **FR-006**: System MUST support sorting via `--sort {title,priority,due,created}` and `--order {asc,desc}` options
- **FR-007**: System MUST assign sequential integer IDs to tasks starting from 1
- **FR-008**: System MUST store tasks in memory only (no persistent storage)
- **FR-009**: System MUST use Python 3.13+ with standard library only
- **FR-010**: System MUST display missing due dates last when using `--sort due --order asc`
- **FR-011**: System MUST display error message but continue execution when invalid task IDs are used (exit code 0)
- **FR-012**: System MUST validate command-line arguments and provide helpful usage information
- **FR-013**: System MUST accept due dates in ISO 8601 format (YYYY-MM-DD) and reject invalid formats
- **FR-014**: System MUST use priority values 1-3 (1=high, 2=medium, 3=low) with default value 1
- **FR-015**: System MUST perform stable sorting (preserving insertion order for tied elements)

### Key Entities

- **Task**: Represents a todo item with ID (sequential integer), description (text), completion status (boolean), priority (integer 1-3, default 1), due date (ISO 8601 format YYYY-MM-DD, optional), and creation timestamp
- **Todo List**: Collection of tasks stored in memory with operations for adding, viewing, updating, deleting, and toggling tasks

## Clarifications

### Session 2026-02-06

- Q: What is the default sort field and order when the user runs `todo list` without any sorting flags? → A: Sort by created time ascending (chronological order)
- Q: What format should due dates follow when entered by the user in the CLI? → A: ISO 8601 format (YYYY-MM-DD)
- Q: What values should the priority field accept and what should be the default priority when creating a task? → A: Integer values 1-3 (1=high, 2=medium, 3=low), default 1
- Q: How should the system handle tie-breaking when two tasks have identical values for the sort field? → A: Preserve insertion order (stable sort)
- Q: What should happen when a user attempts to operate on a task ID that doesn't exist? → A: Display message but continue execution (exit code 0)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All 5 core features (add, list, update, delete, toggle) work via command-line interface without errors
- **SC-002**: Sorting functionality correctly orders tasks by title, priority, due date, or creation date in ascending/descending order
- **SC-003**: Unit tests for all functionality pass with 100% success rate
- **SC-004**: CLI commands accept proper arguments and return appropriate responses within 2 seconds
- **SC-005**: Sequential task IDs are assigned starting from 1 and persist during the session
- **SC-006**: In-memory storage maintains task state during application execution