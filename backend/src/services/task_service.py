from sqlmodel import Session, select, func
from typing import List, Optional
from datetime import datetime, date
from ..models import Task, TaskCreate, TaskUpdate, PriorityEnum
from ..schemas import TaskQueryParams
from fastapi import HTTPException, status


class TaskService:
    """
    Service class for handling business logic related to tasks.
    Provides methods for CRUD operations and ownership enforcement.
    """

    @staticmethod
    def create_task(*, session: Session, task_create: TaskCreate, user_id: str) -> Task:
        """
        Create a new task for the specified user.

        Args:
            session: Database session
            task_create: Task creation data
            user_id: ID of the user creating the task

        Returns:
            Created Task object
        """
        # Create a new task instance
        task = Task.from_orm(task_create) if hasattr(Task, 'from_orm') else Task(**task_create.dict())
        task.user_id = user_id
        task.completed = False  # Default to not completed

        # Add the task to the session and commit
        session.add(task)
        session.commit()
        session.refresh(task)

        return task

    @staticmethod
    def get_task_by_id(*, session: Session, task_id: int, user_id: str) -> Optional[Task]:
        """
        Retrieve a specific task by ID for the specified user.

        Args:
            session: Database session
            task_id: ID of the task to retrieve
            user_id: ID of the user requesting the task

        Returns:
            Task object if found and owned by user, None otherwise

        Raises:
            HTTPException: If the task is not found or not owned by the user
        """
        # Query for the task with the given ID and user_id
        statement = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        task = session.exec(statement).first()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {task_id} not found or not owned by user"
            )

        return task

    @staticmethod
    def get_tasks_by_user(
        *,
        session: Session,
        user_id: str,
        query_params: Optional[TaskQueryParams] = None
    ) -> List[Task]:
        """
        Retrieve all tasks for the specified user with optional filtering and sorting.

        Args:
            session: Database session
            user_id: ID of the user whose tasks to retrieve
            query_params: Optional query parameters for filtering and sorting

        Returns:
            List of Task objects matching the criteria
        """
        # Start with a base query for tasks belonging to the user
        statement = select(Task).where(Task.user_id == user_id)

        # Apply filters based on query parameters
        if query_params:
            # Filter by status
            if query_params.status:
                if query_params.status.lower() == "completed":
                    statement = statement.where(Task.completed == True)
                elif query_params.status.lower() == "pending":
                    statement = statement.where(Task.completed == False)
                elif query_params.status.lower() != "all":
                    # Default to all if invalid status is provided
                    pass

            # Apply sorting
            if query_params.sort:
                sort_field = getattr(Task, query_params.sort, None)
                if sort_field:
                    if query_params.order and query_params.order.lower() == "desc":
                        statement = statement.order_by(sort_field.desc())
                    else:
                        statement = statement.order_by(sort_field.asc())

        # Execute the query
        tasks = session.exec(statement).all()
        return tasks

    @staticmethod
    def update_task(*, session: Session, task_id: int, task_update: TaskUpdate, user_id: str) -> Optional[Task]:
        """
        Update an existing task for the specified user.

        Args:
            session: Database session
            task_id: ID of the task to update
            task_update: Task update data
            user_id: ID of the user updating the task

        Returns:
            Updated Task object if successful, None otherwise

        Raises:
            HTTPException: If the task is not found or not owned by the user
        """
        # Get the existing task
        task = TaskService.get_task_by_id(session=session, task_id=task_id, user_id=user_id)

        # Prepare update data, excluding unset fields
        update_data = task_update.dict(exclude_unset=True)

        # Update the task with the provided data
        for field, value in update_data.items():
            setattr(task, field, value)

        # Update the updated_at timestamp
        task.updated_at = datetime.utcnow()

        # Commit changes to the database
        session.add(task)
        session.commit()
        session.refresh(task)

        return task

    @staticmethod
    def delete_task(*, session: Session, task_id: int, user_id: str) -> bool:
        """
        Delete a task for the specified user.

        Args:
            session: Database session
            task_id: ID of the task to delete
            user_id: ID of the user deleting the task

        Returns:
            True if the task was deleted, False otherwise

        Raises:
            HTTPException: If the task is not found or not owned by the user
        """
        # Get the task to ensure it exists and is owned by the user
        task = TaskService.get_task_by_id(session=session, task_id=task_id, user_id=user_id)

        # Delete the task from the session
        session.delete(task)
        session.commit()

        return True

    @staticmethod
    def patch_task_complete(*, session: Session, task_id: int, completed: bool, user_id: str) -> Optional[Task]:
        """
        Update only the completion status of a task for the specified user.

        Args:
            session: Database session
            task_id: ID of the task to update
            completed: New completion status
            user_id: ID of the user updating the task

        Returns:
            Updated Task object if successful, None otherwise

        Raises:
            HTTPException: If the task is not found or not owned by the user
        """
        # Get the existing task
        task = TaskService.get_task_by_id(session=session, task_id=task_id, user_id=user_id)

        # Update only the completion status
        task.completed = completed
        task.updated_at = datetime.utcnow()

        # Commit changes to the database
        session.add(task)
        session.commit()
        session.refresh(task)

        return task

    @staticmethod
    def count_user_tasks(*, session: Session, user_id: str) -> int:
        """
        Count the total number of tasks for the specified user.

        Args:
            session: Database session
            user_id: ID of the user whose tasks to count

        Returns:
            Total count of tasks for the user
        """
        statement = select(func.count(Task.id)).where(Task.user_id == user_id)
        count = session.exec(statement).one()
        return count

    @staticmethod
    def get_completed_tasks_count(*, session: Session, user_id: str) -> int:
        """
        Count the number of completed tasks for the specified user.

        Args:
            session: Database session
            user_id: ID of the user whose completed tasks to count

        Returns:
            Count of completed tasks for the user
        """
        statement = select(func.count(Task.id)).where(
            Task.user_id == user_id,
            Task.completed == True
        )
        count = session.exec(statement).one()
        return count

    @staticmethod
    def get_pending_tasks_count(*, session: Session, user_id: str) -> int:
        """
        Count the number of pending tasks for the specified user.

        Args:
            session: Database session
            user_id: ID of the user whose pending tasks to count

        Returns:
            Count of pending tasks for the user
        """
        statement = select(func.count(Task.id)).where(
            Task.user_id == user_id,
            Task.completed == False
        )
        count = session.exec(statement).one()
        return count