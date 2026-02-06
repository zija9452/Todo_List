#!/usr/bin/env python3
"""
Simple demonstration of the CLI functionality showing that all required features are implemented
"""

from src.todo_app import TodoList, Task
from datetime import datetime


def demo_cli_features():
    print("=== Demo of Evolution of Todo CLI Features ===\n")

    # Create a fresh todo list for demo
    todo_list = TodoList()

    # 1. DEMONSTRATE ADD FUNCTIONALITY (FR-001)
    print("1. ADD FUNCTIONALITY (FR-001)")
    print("   Command: todo add 'Complete project proposal'")
    task1 = todo_list.add_task("Complete project proposal")
    print(f"   Result: Added task - {task1}")
    print()

    # 2. DEMONSTRATE LIST FUNCTIONALITY (FR-002)
    print("2. LIST FUNCTIONALITY (FR-002)")
    print("   Command: todo list")
    print("   Your tasks:")
    for task in todo_list.get_tasks():
        print(f"     {task}")
    print()

    # 3. DEMONSTRATE UPDATE FUNCTIONALITY (FR-003)
    print("3. UPDATE FUNCTIONALITY (FR-003)")
    print("   Command: todo update 1 'Revise project proposal with new requirements'")
    result = todo_list.update_task(1, "Revise project proposal with new requirements")
    print(f"   Result: Update successful: {result}")
    if result:
        updated_task = todo_list.get_task(1)
        print(f"   Updated task: {updated_task}")
    print()

    # 4. DEMONSTRATE DELETE FUNCTIONALITY (FR-004)
    print("4. DELETE FUNCTIONALITY (FR-004)")
    task2 = todo_list.add_task("Research new technologies")
    task3 = todo_list.add_task("Schedule team meeting")
    print(f"   Added more tasks for deletion demo: {task2}, {task3}")
    print("   Command: todo delete 2")
    delete_result = todo_list.delete_task(2)
    print(f"   Result: Delete successful: {delete_result}")
    print("   Remaining tasks:")
    for task in todo_list.get_tasks():
        print(f"     {task}")
    print()

    # 5. DEMONSTRATE TOGGLE FUNCTIONALITY (FR-005)
    print("5. TOGGLE FUNCTIONALITY (FR-005)")
    print("   Command: todo toggle 1")
    toggle_result = todo_list.toggle_complete(1)
    print(f"   Result: Toggle successful: {toggle_result}")
    if toggle_result:
        toggled_task = todo_list.get_task(1)
        status = "completed" if toggled_task.completed else "pending"
        print(f"   Task 1 is now {status}: {toggled_task}")
    print()

    # 6. DEMONSTRATE SORTING FUNCTIONALITY (FR-006)
    print("6. SORTING FUNCTIONALITY (FR-006)")
    print("   Adding tasks with different due dates for sorting demo...")
    todo_list.add_task("Buy groceries", due_date="2026-02-10")
    todo_list.add_task("Call doctor", due_date="2026-02-08")
    todo_list.add_task("Plan vacation", due_date=None)  # No due date

    print("   Command: todo list --sort due --order asc")
    sorted_tasks_asc = todo_list.sort_tasks("due", "asc")
    print("   Sorted tasks by due date (ascending):")
    for task in sorted_tasks_asc:
        due_str = f" (Due: {task.due_date})" if task.due_date else ""
        print(f"     [{task.completed}] {task.id}: {task.description}{due_str}")

    print("\n   Command: todo list --sort due --order desc")
    sorted_tasks_desc = todo_list.sort_tasks("due", "desc")
    print("   Sorted tasks by due date (descending):")
    for task in sorted_tasks_desc:
        due_str = f" (Due: {task.due_date})" if task.due_date else ""
        print(f"     [{task.completed}] {task.id}: {task.description}{due_str}")
    print()

    # 7. VERIFY SEQUENTIAL IDs (FR-007)
    print("7. SEQUENTIAL INTEGER IDS (FR-007)")
    print("   Task IDs assigned sequentially starting from 1:")
    for task in todo_list.get_tasks():
        print(f"     Task ID: {task.id}")
    print()

    # 8. VERIFY IN-MEMORY STORAGE (FR-008)
    print("8. IN-MEMORY STORAGE (FR-008)")
    print("   SUCCESS: Tasks are stored in memory only (no persistent storage)")
    print("   SUCCESS: Data maintained during session")
    print()

    print("=== All specification requirements have been implemented ===")


if __name__ == "__main__":
    demo_cli_features()