# Data Model: Evolution of Todo CLI App

## Entity Definitions

### Task
Represents a single todo item with the following attributes:

**Attributes**:
- `id`: Sequential integer, positive, immutable after creation, starting from 1
- `description`: String, required, maximum 500 characters
- `completed`: Boolean, default false
- `priority`: Integer, values 1-3 (1=high, 2=medium, 3=low), default 1
- `due_date`: String, optional, ISO 8601 format (YYYY-MM-DD) or None
- `created_at`: Datetime, immutable after creation, in ISO format

**Validation Rules**:
- ID must be unique within the Todo List instance
- Description must not be empty
- Priority must be in range [1, 2, 3]
- Due date, if provided, must be in valid ISO 8601 format

**State Transitions**:
- `completed` can transition from false to true (toggle completion)
- `completed` can transition from true to false (toggle back to incomplete)

### TodoList
Represents a collection of Task objects with operations:

**Operations**:
- `add_task(description, priority=1, due_date=None)`: Creates new Task with next available ID
- `delete_task(id)`: Removes Task by ID, returns boolean for success
- `update_task(id, description, priority=None, due_date=None)`: Modifies Task attributes, returns boolean for success
- `toggle_completion(id)`: Flips completed status, returns boolean for success
- `get_task(id)`: Retrieves Task by ID, returns Task or None
- `get_all_tasks()`: Returns all Tasks in creation order
- `sort_tasks(sort_field, order)`: Returns sorted Tasks based on field and direction

## Relationships
- TodoList contains 0..n Task objects
- Each Task belongs to exactly one TodoList during its lifetime

## Data Flow
1. User input → validation → Task creation/update
2. Internal operations → sorting algorithms → filtered/ordered views
3. Display layer → serialization → user output