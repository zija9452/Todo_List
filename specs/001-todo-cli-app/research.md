# Research: Evolution of Todo CLI App

## Decision Log

### CLI Framework Choice
**Decision**: Use Python's standard library `argparse` module
**Rationale**: Aligns with constitution requirement for stdlib only; provides robust argument parsing capabilities; widely adopted standard solution
**Alternatives considered**:
- Click library (rejected - violates stdlib-only constraint)
- Sys.argv manual parsing (rejected - reinventing standard solution unnecessarily)

### Data Model Implementation
**Decision**: Single Task class with in-memory list storage
**Rationale**: Matches requirement for in-memory storage only; simple, efficient for CLI application; supports all required attributes (ID, description, status, priority, due date)
**Alternatives considered**:
- Multiple classes with relationships (rejected - overengineering for simple CLI app)
- Dictionary-based storage (rejected - less maintainable than class-based approach)

### Sorting Algorithm
**Decision**: Use Python's built-in `sorted()` function with custom key functions
**Rationale**: Provides stable sort (required by spec); leverages Python's efficient Timsort algorithm; supports all required sort fields and directions
**Alternatives considered**:
- Custom sorting implementation (rejected - reinventing standard solution)
- Third-party sorting libraries (rejected - violates stdlib-only constraint)

### Priority Value Mapping
**Decision**: Integer values 1-3 (1=high, 2=medium, 3=low) with default of 1
**Rationale**: Matches specification requirement; simple numeric system that's intuitive; default priority of 1 ensures tasks start with highest priority
**Alternatives considered**:
- Text values (high/medium/low) (rejected - more complex parsing needed)
- Reverse mapping (1=low, 3=high) (rejected - counterintuitive)

### Date Format Handling
**Decision**: ISO 8601 format (YYYY-MM-DD) with datetime parsing
**Rationale**: Matches specification requirement; unambiguous format; standard international format; supports proper sorting
**Alternatives considered**:
- Multiple format support (rejected - adds complexity without clear benefit)
- Unix timestamps (rejected - not user-friendly for CLI input)

### Error Handling Strategy
**Decision**: Display error message but continue execution (exit code 0) for invalid task IDs
**Rationale**: Matches specification requirement; provides user feedback without disrupting workflow; maintains application availability
**Alternatives considered**:
- Exit with error code (rejected - contradicts spec requirement)
- Silent failure (rejected - provides no user feedback)