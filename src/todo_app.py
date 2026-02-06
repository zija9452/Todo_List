#!/usr/bin/env python3
"""
Todo List Application
Phase I: In-Memory Python Console App

Supports the following operations:
- Add Task
- Delete Task
- Update Task
- View Task List
- Toggle Complete
- Sort Task List
"""

import argparse
import sys
from typing import List, Dict, Optional
from datetime import datetime


class Task:
    def __init__(self, id: int, description: str, completed: bool = False, priority: int = 1, due_date: Optional[str] = None):
        self.id = id
        self.description = description
        self.completed = completed
        self.priority = priority
        self.due_date = due_date  # Format: YYYY-MM-DD or None
        self.created_at = datetime.now()

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "description": self.description,
            "completed": self.completed,
            "priority": self.priority,
            "due_date": self.due_date,
            "created_at": self.created_at.isoformat()
        }

    def __str__(self) -> str:
        status = "X" if self.completed else "O"
        due_str = f" (Due: {self.due_date})" if self.due_date else ""
        return f"[{status}] {self.id}: {self.description}{due_str}"


class TodoList:
    def __init__(self):
        self.tasks: List[Task] = []
        self.next_id = 1

    def add_task(self, description: str, priority: int = 1, due_date: Optional[str] = None) -> Task:
        task = Task(self.next_id, description, priority=priority, due_date=due_date)
        self.tasks.append(task)
        self.next_id += 1
        return task

    def delete_task(self, task_id: int) -> bool:
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                return True
        return False

    def update_task(self, task_id: int, description: str, priority: Optional[int] = None, due_date: Optional[str] = None) -> bool:
        for task in self.tasks:
            if task.id == task_id:
                task.description = description
                if priority is not None:
                    task.priority = priority
                if due_date is not None:
                    task.due_date = due_date
                return True
        return False

    def toggle_complete(self, task_id: int) -> bool:
        for task in self.tasks:
            if task.id == task_id:
                task.completed = not task.completed  # Toggle the status
                return True
        return False

    def get_tasks(self) -> List[Task]:
        return self.tasks

    def get_task(self, task_id: int) -> Optional[Task]:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def sort_tasks(self, sort_by: str = "created", order: str = "asc") -> List[Task]:
        """Sort tasks by specified attribute in ascending or descending order."""
        reverse_order = order.lower() == "desc"

        if sort_by == "title":
            # Sort by description
            sorted_tasks = sorted(self.tasks, key=lambda t: t.description.lower(), reverse=reverse_order)
        elif sort_by == "priority":
            # Sort by priority
            sorted_tasks = sorted(self.tasks, key=lambda t: t.priority, reverse=reverse_order)
        elif sort_by == "due":
            # Sort by due date, putting None values last for ascending order
            def sort_key(task):
                if task.due_date is None:
                    # For ascending order, None should come last
                    # So we return a large date for None values
                    return datetime.max if not reverse_order else datetime.min
                try:
                    return datetime.strptime(task.due_date, "%Y-%m-%d")
                except ValueError:
                    # If date parsing fails, treat as None
                    return datetime.max if not reverse_order else datetime.min

            sorted_tasks = sorted(self.tasks, key=sort_key, reverse=reverse_order)
        elif sort_by == "created":
            # Sort by creation time
            sorted_tasks = sorted(self.tasks, key=lambda t: t.created_at, reverse=reverse_order)
        else:
            # Default: sort by ID
            sorted_tasks = sorted(self.tasks, key=lambda t: t.id, reverse=reverse_order)

        return sorted_tasks


def parse_command(user_input: str):
    """Parse user input into command and arguments, handling quoted strings and flags."""
    import shlex

    try:
        parts = shlex.split(user_input.strip())
    except ValueError:
        # If shlex fails, fall back to simple split
        parts = user_input.strip().split()

    if not parts:
        return None, []

    command = parts[0].lower()
    args = parts[1:]

    return command, args


def main():
    # Check if command line arguments are provided (non-interactive mode)
    if len(sys.argv) > 1:
        # Use argparse for command line mode
        parser = argparse.ArgumentParser(description="Todo List Application")
        subparsers = parser.add_subparsers(dest='command', help='Available commands')

        # Add command
        add_parser = subparsers.add_parser('add', help='Add a new task')
        add_parser.add_argument('description', nargs='+', help='Task description')

        # List command
        list_parser = subparsers.add_parser('list', help='List all tasks')
        list_parser.add_argument('--sort', choices=['title', 'priority', 'due', 'created'], default='created', help='Sort by attribute')
        list_parser.add_argument('--order', choices=['asc', 'desc'], default='asc', help='Sort order')

        # Update command
        update_parser = subparsers.add_parser('update', help='Update a task')
        update_parser.add_argument('id', type=int, help='Task ID')
        update_parser.add_argument('description', nargs='+', help='New task description')

        # Delete command
        delete_parser = subparsers.add_parser('delete', help='Delete a task')
        delete_parser.add_argument('id', type=int, help='Task ID')

        # Toggle command
        toggle_parser = subparsers.add_parser('toggle', help='Toggle task completion status')
        toggle_parser.add_argument('id', type=int, help='Task ID')

        args = parser.parse_args()

        # Initialize in-memory storage
        todo_list = TodoList()

        if args.command == 'add':
            description = ' '.join(args.description)
            task = todo_list.add_task(description)
            print(f"Added task: {task}")
        elif args.command == 'list':
            sorted_tasks = todo_list.sort_tasks(args.sort, args.order)
            if sorted_tasks:
                print("Your tasks:")
                for task in sorted_tasks:
                    print(f"  {task}")
            else:
                print("No tasks in the list")
        elif args.command == 'update':
            description = ' '.join(args.description)
            if todo_list.update_task(args.id, description):
                task = todo_list.get_task(args.id)
                print(f"Updated task: {task}")
            else:
                print(f"No task found with ID {args.id}")
        elif args.command == 'delete':
            if todo_list.delete_task(args.id):
                print(f"Deleted task with ID {args.id}")
            else:
                print(f"No task found with ID {args.id}")
        elif args.command == 'toggle':
            if todo_list.toggle_complete(args.id):
                task = todo_list.get_task(args.id)
                status = "completed" if task.completed else "pending"
                print(f"Toggled task {args.id} to {status}")
            else:
                print(f"No task found with ID {args.id}")
        else:
            parser.print_help()
    else:
        # Interactive mode
        todo_list = TodoList()
        print("Welcome to the Todo List Console Application!")
        print("Available commands: add, list, update, delete, toggle, quit, help")
        print("Example: add Complete project documentation")
        print("         list --sort title --order asc")
        print("         update 1 Revised project documentation")
        print("         toggle 1")
        print("         delete 1")

        while True:
            try:
                user_input = input("\n> ").strip()

                if not user_input:
                    continue

                command, args = parse_command(user_input)

                if command == 'quit' or command == 'exit':
                    print("Goodbye!")
                    break
                elif command == 'help':
                    print("Available commands:")
                    print("  add <description> - Add a new task")
                    print("  list [--sort title|priority|due|created] [--order asc|desc] - List tasks")
                    print("  update <id> <description> - Update a task")
                    print("  delete <id> - Delete a task")
                    print("  toggle <id> - Toggle completion status")
                    print("  quit/exit - Exit the application")
                    print("  help - Show this help message")
                elif command == 'add':
                    if len(args) == 0:
                        print("Usage: add <description>")
                    else:
                        description = ' '.join(args)
                        task = todo_list.add_task(description)
                        print(f"Added task: {task}")
                elif command == 'list':
                    # Parse additional arguments for sort and order
                    sort_arg_index = -1
                    order_arg_index = -1

                    sort_by = 'created'
                    order = 'asc'

                    for i, arg in enumerate(args):
                        if arg == '--sort' and i + 1 < len(args):
                            sort_by = args[i + 1]
                        elif arg == '--order' and i + 1 < len(args):
                            order = args[i + 1]

                    sorted_tasks = todo_list.sort_tasks(sort_by, order)
                    if sorted_tasks:
                        print("Your tasks:")
                        for task in sorted_tasks:
                            print(f"  {task}")
                    else:
                        print("No tasks in the list")
                elif command == 'update':
                    if len(args) < 2:
                        print("Usage: update <id> <description>")
                    else:
                        try:
                            task_id = int(args[0])
                            description = ' '.join(args[1:])

                            if todo_list.update_task(task_id, description):
                                task = todo_list.get_task(task_id)
                                print(f"Updated task: {task}")
                            else:
                                print(f"No task found with ID {task_id}")
                        except ValueError:
                            print("Task ID must be a number")
                elif command == 'delete':
                    if len(args) != 1:
                        print("Usage: delete <id>")
                    else:
                        try:
                            task_id = int(args[0])

                            if todo_list.delete_task(task_id):
                                print(f"Deleted task with ID {task_id}")
                            else:
                                print(f"No task found with ID {task_id}")
                        except ValueError:
                            print("Task ID must be a number")
                elif command == 'toggle':
                    if len(args) != 1:
                        print("Usage: toggle <id>")
                    else:
                        try:
                            task_id = int(args[0])

                            if todo_list.toggle_complete(task_id):
                                task = todo_list.get_task(task_id)
                                status = "completed" if task.completed else "pending"
                                print(f"Toggled task {task_id} to {status}")
                            else:
                                print(f"No task found with ID {task_id}")
                        except ValueError:
                            print("Task ID must be a number")
                else:
                    print(f"Unknown command: {command}. Type 'help' for available commands.")

            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                print("\nGoodbye!")
                break


if __name__ == "__main__":
    main()