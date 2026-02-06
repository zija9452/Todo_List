# Quickstart Guide: Evolution of Todo CLI App

## Prerequisites
- Python 3.13 or higher
- pip or uv package manager
- Windows, Linux, or macOS operating system

## Setup
1. Clone or download the repository
2. Navigate to the project directory
3. Install dependencies: `pip install -e .` or `uv pip install .`

## Basic Usage

### Adding Tasks
```bash
python -m src.todo_app add "Complete project proposal"
```

### Listing Tasks
```bash
python -m src.todo_app list
# By default, lists tasks sorted by creation time ascending
```

### Updating Tasks
```bash
python -m src.todo_app update 1 "Revise project proposal with new requirements"
```

### Deleting Tasks
```bash
python -m src.todo_app delete 1
```

### Toggling Completion Status
```bash
python -m src.todo_app toggle 1
```

### Sorting Tasks
```bash
# Sort by title (ascending)
python -m src.todo_app list --sort title --order asc

# Sort by priority (descending)
python -m src.todo_app list --sort priority --order desc

# Sort by due date (ascending - earliest first, missing dates last)
python -m src.todo_app list --sort due --order asc

# Sort by creation time (descending - newest first)
python -m src.todo_app list --sort created --order desc
```

## Example Workflow
```bash
# Add tasks
python -m src.todo_app add "Prepare presentation slides"
python -m src.todo_app add "Review code changes" --priority 2 --due-date "2026-02-10"
python -m src.todo_app add "Schedule team meeting" --priority 3

# List all tasks
python -m src.todo_app list

# Sort by priority to see most important tasks first
python -m src.todo_app list --sort priority --order desc

# Mark a task as completed
python -m src.todo_app toggle 1

# Update a task
python -m src.todo_app update 2 "Review code changes with security team"

# List sorted by due date to see upcoming deadlines
python -m src.todo_app list --sort due --order asc
```

## Testing
Run all unit tests with:
```bash
python -m pytest tests/ -v
```

## Troubleshooting
- If commands fail with "invalid choice", check the available commands and options
- For date format issues, ensure dates are in YYYY-MM-DD format
- For priority issues, use integer values 1 (high), 2 (medium), or 3 (low)