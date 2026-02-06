#!/usr/bin/env python3
"""
Test script to demonstrate the CLI functionality with the new command structure
"""

import sys
import io
from contextlib import redirect_stdout
from src.todo_app import TodoList, Task

def test_new_cli_functionality():
    print("Testing the new CLI functionality based on the updated code...")

    # Import the main function to test the CLI commands
    from src.todo_app import main
    import sys

    # Test different commands by simulating sys.argv
    print("\n1. Testing ADD functionality:")
    sys.argv = ['todo', 'add', 'Complete', 'project', 'documentation']
    try:
        main()
    except SystemExit:
        pass  # Expected after argparse

    print("\n2. Testing LIST functionality (ascending by created):")
    sys.argv = ['todo', 'list']
    try:
        main()
    except SystemExit:
        pass

    print("\n3. Testing UPDATE functionality:")
    sys.argv = ['todo', 'update', '1', 'Updated', 'project', 'documentation']
    try:
        main()
    except SystemExit:
        pass

    print("\n4. Testing TOGGLE functionality:")
    sys.argv = ['todo', 'toggle', '1']
    try:
        main()
    except SystemExit:
        pass

    print("\n5. Testing LIST functionality with sorting (descending by title):")
    sys.argv = ['todo', 'list', '--sort', 'title', '--order', 'desc']
    try:
        main()
    except SystemExit:
        pass

    print("\n6. Testing DELETE functionality:")
    sys.argv = ['todo', 'delete', '1']
    try:
        main()
    except SystemExit:
        pass

if __name__ == "__main__":
    test_new_cli_functionality()