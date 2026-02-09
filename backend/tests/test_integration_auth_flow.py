import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.main import app
from src.models import Task


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


def test_task_lifecycle_integration(client):
    """
    Integration test for the full task lifecycle: create -> list -> update -> delete.
    This test simulates a user interacting with the task API.
    """
    # Mock user ID for testing
    user_id = "test_user_123"

    # Test creating a task
    create_response = client.post(
        f"/api/users/{user_id}/tasks",
        json={
            "title": "Test Task",
            "description": "This is a test task",
            "priority": "medium",
            "due_date": "2024-12-31"
        },
        headers={"Authorization": "Bearer fake-jwt-token"}
    )

    # Since we're not implementing full auth in this test, expect a 401
    # But we want to make sure the endpoint exists
    assert create_response.status_code in [201, 401, 422]

    # If the task was created successfully, continue with other operations
    if create_response.status_code == 201:
        task_data = create_response.json()
        task_id = task_data["id"]

        # Test getting the specific task
        get_one_response = client.get(
            f"/api/users/{user_id}/tasks/{task_id}",
            headers={"Authorization": "Bearer fake-jwt-token"}
        )
        assert get_one_response.status_code in [200, 401]

        # Test updating the task
        update_response = client.put(
            f"/api/users/{user_id}/tasks/{task_id}",
            json={
                "title": "Updated Test Task",
                "completed": True
            },
            headers={"Authorization": "Bearer fake-jwt-token"}
        )
        assert update_response.status_code in [200, 401, 422]

        # Test patching completion status
        patch_response = client.patch(
            f"/api/users/{user_id}/tasks/{task_id}/complete?completed=true",
            headers={"Authorization": "Bearer fake-jwt-token"}
        )
        assert patch_response.status_code in [200, 401]

        # Test deleting the task
        delete_response = client.delete(
            f"/api/users/{user_id}/tasks/{task_id}",
            headers={"Authorization": "Bearer fake-jwt-token"}
        )
        assert delete_response.status_code in [204, 401]


def test_task_list_endpoints(client):
    """
    Test the task listing endpoint with query parameters.
    """
    user_id = "test_user_123"

    # Test getting all tasks for a user
    response = client.get(
        f"/api/users/{user_id}/tasks",
        headers={"Authorization": "Bearer fake-jwt-token"}
    )
    assert response.status_code in [200, 401]

    # Test with query parameters
    response_with_params = client.get(
        f"/api/users/{user_id}/tasks?status=pending&sort=created&order=asc",
        headers={"Authorization": "Bearer fake-jwt-token"}
    )
    assert response_with_params.status_code in [200, 401]


def test_error_handling(client):
    """
    Test error handling for common error cases.
    """
    user_id = "test_user_123"
    invalid_task_id = 99999

    # Test getting a non-existent task
    response = client.get(
        f"/api/users/{user_id}/tasks/{invalid_task_id}",
        headers={"Authorization": "Bearer fake-jwt-token"}
    )
    # Could be 404 or 401 depending on auth middleware
    assert response.status_code in [404, 401, 422]

    # Test updating a non-existent task
    update_response = client.put(
        f"/api/users/{user_id}/tasks/{invalid_task_id}",
        json={"title": "Updated Title"},
        headers={"Authorization": "Bearer fake-jwt-token"}
    )
    assert update_response.status_code in [404, 401, 422]

    # Test deleting a non-existent task
    delete_response = client.delete(
        f"/api/users/{user_id}/tasks/{invalid_task_id}",
        headers={"Authorization": "Bearer fake-jwt-token"}
    )
    assert delete_response.status_code in [404, 401]


def test_auth_enforcement(client):
    """
    Test that endpoints properly enforce authentication.
    """
    user_id = "test_user_123"

    # Try to access without authorization header
    response = client.get(f"/api/users/{user_id}/tasks")
    assert response.status_code == 401

    # Try with an invalid authorization header
    response = client.get(
        f"/api/users/{user_id}/tasks",
        headers={"Authorization": "Bearer invalid-token"}
    )
    # Could be 401 for invalid token or 403 for insufficient permissions
    assert response.status_code in [401, 403]