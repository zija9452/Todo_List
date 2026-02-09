from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List, Optional
from ..db import get_session
from ..models import Task
from ..schemas import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse, TaskQueryParams
from ..auth import get_current_user, verify_user_owns_resource, TokenData
from ..services.task_service import TaskService

router = APIRouter(prefix="/api", tags=["tasks"])


@router.post("/users/{user_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: str,
    task_create: TaskCreate,
    current_user: TokenData = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Create a new task for the specified user.

    Args:
        user_id: The ID of the user for whom to create the task
        task_create: Task creation data
        current_user: The currently authenticated user (extracted from JWT)
        session: Database session

    Returns:
        Created task as TaskResponse

    Raises:
        HTTPException: If the user is not authorized to create tasks for the specified user
    """
    # Verify that the current user is authorized to create tasks for the specified user
    verify_user_owns_resource(current_user, user_id)

    # Create the task using the service
    task = TaskService.create_task(session=session, task_create=task_create, user_id=user_id)

    return task


@router.get("/users/{user_id}/tasks", response_model=TaskListResponse)
async def get_tasks(
    user_id: str,
    status_param: Optional[str] = Query(None, alias="status", description="Filter by status: all|pending|completed"),
    sort: Optional[str] = Query(None, description="Sort by: created|title|due_date"),
    order: Optional[str] = Query(None, description="Order: asc|desc"),
    current_user: TokenData = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> TaskListResponse:
    """
    Get all tasks for the specified user with optional filtering and sorting.

    Args:
        user_id: The ID of the user whose tasks to retrieve
        status_param: Filter by status: all|pending|completed
        sort: Sort by: created|title|due_date
        order: Order: asc|desc
        current_user: The currently authenticated user (extracted from JWT)
        session: Database session

    Returns:
        List of tasks as TaskListResponse

    Raises:
        HTTPException: If the user is not authorized to access tasks for the specified user
    """
    # Verify that the current user is authorized to access tasks for the specified user
    verify_user_owns_resource(current_user, user_id)

    # Prepare query parameters
    query_params = TaskQueryParams(status=status_param, sort=sort, order=order)

    # Get tasks using the service
    tasks = TaskService.get_tasks_by_user(session=session, user_id=user_id, query_params=query_params)

    # Convert to response format
    task_responses = [TaskResponse.from_orm(task) if hasattr(TaskResponse, 'from_orm') else TaskResponse(**task.dict()) for task in tasks]

    return TaskListResponse(tasks=task_responses)


@router.get("/users/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: str,
    task_id: int,
    current_user: TokenData = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Get a specific task by ID for the specified user.

    Args:
        user_id: The ID of the user whose task to retrieve
        task_id: The ID of the task to retrieve
        current_user: The currently authenticated user (extracted from JWT)
        session: Database session

    Returns:
        Task as TaskResponse

    Raises:
        HTTPException: If the task is not found or the user is not authorized to access it
    """
    # Verify that the current user is authorized to access tasks for the specified user
    verify_user_owns_resource(current_user, user_id)

    # Get the task using the service
    task = TaskService.get_task_by_id(session=session, task_id=task_id, user_id=user_id)

    return TaskResponse.from_orm(task) if hasattr(TaskResponse, 'from_orm') else TaskResponse(**task.dict())


@router.put("/users/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: str,
    task_id: int,
    task_update: TaskUpdate,
    current_user: TokenData = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Update a specific task by ID for the specified user.

    Args:
        user_id: The ID of the user whose task to update
        task_id: The ID of the task to update
        task_update: Task update data
        current_user: The currently authenticated user (extracted from JWT)
        session: Database session

    Returns:
        Updated task as TaskResponse

    Raises:
        HTTPException: If the task is not found or the user is not authorized to update it
    """
    # Verify that the current user is authorized to update tasks for the specified user
    verify_user_owns_resource(current_user, user_id)

    # Update the task using the service
    updated_task = TaskService.update_task(
        session=session,
        task_id=task_id,
        task_update=task_update,
        user_id=user_id
    )

    return TaskResponse.from_orm(updated_task) if hasattr(TaskResponse, 'from_orm') else TaskResponse(**updated_task.dict())


@router.delete("/users/{user_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    user_id: str,
    task_id: int,
    current_user: TokenData = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> None:
    """
    Delete a specific task by ID for the specified user.

    Args:
        user_id: The ID of the user whose task to delete
        task_id: The ID of the task to delete
        current_user: The currently authenticated user (extracted from JWT)
        session: Database session

    Raises:
        HTTPException: If the task is not found or the user is not authorized to delete it
    """
    # Verify that the current user is authorized to delete tasks for the specified user
    verify_user_owns_resource(current_user, user_id)

    # Delete the task using the service
    TaskService.delete_task(session=session, task_id=task_id, user_id=user_id)


@router.patch("/users/{user_id}/tasks/{task_id}/complete", response_model=TaskResponse)
async def patch_task_complete(
    user_id: str,
    task_id: int,
    completed: bool = Query(..., description="New completion status for the task"),
    current_user: TokenData = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Update only the completion status of a specific task by ID for the specified user.

    Args:
        user_id: The ID of the user whose task completion status to update
        task_id: The ID of the task to update
        completed: New completion status for the task
        current_user: The currently authenticated user (extracted from JWT)
        session: Database session

    Returns:
        Updated task as TaskResponse

    Raises:
        HTTPException: If the task is not found or the user is not authorized to update it
    """
    # Verify that the current user is authorized to update tasks for the specified user
    verify_user_owns_resource(current_user, user_id)

    # Update the task completion status using the service
    updated_task = TaskService.patch_task_complete(
        session=session,
        task_id=task_id,
        completed=completed,
        user_id=user_id
    )

    return TaskResponse.from_orm(updated_task) if hasattr(TaskResponse, 'from_orm') else TaskResponse(**updated_task.dict())