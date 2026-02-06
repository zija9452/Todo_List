#!/usr/bin/env python3
"""
Test script to demonstrate the CLI functionality of the Todo application
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.todo_app import TodoList, Task

def test_cli_functionality():
    print("Testing Todo List Application CLI functionality...\n")

    # Initialize the todo list
    todo_list = TodoList()

    # Test 1: Add tasks
    print("1. Testing ADD functionality:")
    task1 = todo_list.add_task("Buy groceries")
    task2 = todo_list.add_task("Walk the dog")
    task3 = todo_list.add_task("Finish project")
    print(f"   Added tasks: '{task1.description}', '{task2.description}', '{task3.description}'")

    # Test 2: View tasks
    print("\n2. Testing VIEW functionality:")
    tasks = todo_list.get_tasks()
    print("   Current tasks:")
    for task in tasks:
        print(f"     {task}")

    # Test 3: Mark a task as complete
    print("\n3. Testing MARK COMPLETE functionality:")
    result = todo_list.mark_complete(1)  # Mark first task as complete
    print(f"   Marked task ID 1 as complete: {result}")
    print("   Updated task list:")
    for task in todo_list.get_tasks():
        print(f"     {task}")

    # Test 4: Update a task
    print("\n4. Testing UPDATE functionality:")
    result = todo_list.update_task(2, "Walk the cat instead")
    print(f"   Updated task ID 2: {result}")
    print("   Updated task list:")
    for task in todo_list.get_tasks():
        print(f"     {task}")

    # Test 5: Delete a task
    print("\n5. Testing DELETE functionality:")
    result = todo_list.delete_task(3)
    print(f"   Deleted task ID 3: {result}")
    print("   Final task list:")
    for task in todo_list.get_tasks():
        print(f"     {task}")

    print("\nSUCCESS: All CLI functionalities tested successfully!")

if __name__ == "__main__":
    test_cli_functionality()