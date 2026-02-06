import unittest
from src.todo_app import TodoList, Task
from datetime import datetime


class TestTodoList(unittest.TestCase):

    def setUp(self):
        self.todo_list = TodoList()

    def test_add_task(self):
        task = self.todo_list.add_task("Test task")
        self.assertEqual(len(self.todo_list.get_tasks()), 1)
        self.assertEqual(task.description, "Test task")
        self.assertFalse(task.completed)
        self.assertEqual(task.id, 1)
        self.assertIsNotNone(task.created_at)

    def test_add_task_with_priority_and_due_date(self):
        task = self.todo_list.add_task("Test task", priority=2, due_date="2026-12-31")
        self.assertEqual(task.priority, 2)
        self.assertEqual(task.due_date, "2026-12-31")

    def test_delete_task(self):
        task = self.todo_list.add_task("Test task")
        result = self.todo_list.delete_task(task.id)
        self.assertTrue(result)
        self.assertEqual(len(self.todo_list.get_tasks()), 0)

    def test_delete_nonexistent_task(self):
        result = self.todo_list.delete_task(999)
        self.assertFalse(result)

    def test_update_task(self):
        task = self.todo_list.add_task("Original task")
        result = self.todo_list.update_task(task.id, "Updated task")
        self.assertTrue(result)

        updated_task = self.todo_list.get_task(task.id)
        self.assertEqual(updated_task.description, "Updated task")

    def test_toggle_complete(self):
        task = self.todo_list.add_task("Test task")
        # Initially not completed
        self.assertFalse(task.completed)

        # Toggle to complete
        result = self.todo_list.toggle_complete(task.id)
        self.assertTrue(result)
        self.assertTrue(task.completed)

        # Toggle back to incomplete
        result = self.todo_list.toggle_complete(task.id)
        self.assertTrue(result)
        self.assertFalse(task.completed)

    def test_get_task(self):
        task = self.todo_list.add_task("Test task")
        retrieved = self.todo_list.get_task(task.id)
        self.assertEqual(retrieved, task)

    def test_get_nonexistent_task(self):
        retrieved = self.todo_list.get_task(999)
        self.assertIsNone(retrieved)

    def test_sort_tasks_by_title(self):
        task1 = self.todo_list.add_task("Zebra task")
        task2 = self.todo_list.add_task("Apple task")
        task3 = self.todo_list.add_task("Mango task")

        # Test ascending sort by title
        sorted_tasks = self.todo_list.sort_tasks("title", "asc")
        titles = [t.description for t in sorted_tasks]
        self.assertEqual(titles, ["Apple task", "Mango task", "Zebra task"])

        # Test descending sort by title
        sorted_tasks_desc = self.todo_list.sort_tasks("title", "desc")
        titles_desc = [t.description for t in sorted_tasks_desc]
        self.assertEqual(titles_desc, ["Zebra task", "Mango task", "Apple task"])

    def test_sort_tasks_by_priority(self):
        task1 = self.todo_list.add_task("Low priority", priority=1)
        task2 = self.todo_list.add_task("High priority", priority=3)
        task3 = self.todo_list.add_task("Medium priority", priority=2)

        # Test ascending sort by priority
        sorted_tasks = self.todo_list.sort_tasks("priority", "asc")
        priorities = [t.priority for t in sorted_tasks]
        self.assertEqual(priorities, [1, 2, 3])

        # Test descending sort by priority
        sorted_tasks_desc = self.todo_list.sort_tasks("priority", "desc")
        priorities_desc = [t.priority for t in sorted_tasks_desc]
        self.assertEqual(priorities_desc, [3, 2, 1])

    def test_sort_tasks_by_created(self):
        task1 = self.todo_list.add_task("First task")
        task2 = self.todo_list.add_task("Second task")
        task3 = self.todo_list.add_task("Third task")

        # Test ascending sort by creation time (by ID since created_at is set during add)
        sorted_tasks = self.todo_list.sort_tasks("created", "asc")
        ids = [t.id for t in sorted_tasks]
        self.assertEqual(ids, [1, 2, 3])

        # Test descending sort by creation time
        sorted_tasks_desc = self.todo_list.sort_tasks("created", "desc")
        ids_desc = [t.id for t in sorted_tasks_desc]
        self.assertEqual(ids_desc, [3, 2, 1])

    def test_sort_tasks_by_due_date(self):
        task1 = self.todo_list.add_task("Task 1", due_date="2026-12-31")
        task2 = self.todo_list.add_task("Task 2", due_date="2026-01-01")  # Earlier date
        task3 = self.todo_list.add_task("Task 3")  # No due date

        # Test ascending sort by due date (earlier dates first, no date last)
        sorted_tasks = self.todo_list.sort_tasks("due", "asc")
        due_dates = [t.due_date for t in sorted_tasks]
        # task2 (2026-01-01) should come first, task1 (2026-12-31) second, task3 (None) last
        self.assertEqual(due_dates, ["2026-01-01", "2026-12-31", None])

        # Test descending sort by due date (later dates first, no date last)
        sorted_tasks_desc = self.todo_list.sort_tasks("due", "desc")
        due_dates_desc = [t.due_date for t in sorted_tasks_desc]
        # task1 (2026-12-31) should come first, task2 (2026-01-01) second, task3 (None) last
        self.assertEqual(due_dates_desc, ["2026-12-31", "2026-01-01", None])


if __name__ == '__main__':
    unittest.main()