#!/bin/bash

# Script to verify data persistence in the Todo application
echo "Starting persistence verification test..."

# Check if backend is running
if ! pgrep -f "uvicorn.*main:app" > /dev/null; then
    echo "Starting backend server..."
    cd backend
    nohup uvicorn src.main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
    BACKEND_PID=$!
    sleep 5  # Wait for server to start
    cd ..
else
    echo "Backend server is already running."
fi

echo "Backend server started."

# Create a test task
echo "Creating a test task..."
TASK_RESPONSE=$(curl -X POST http://localhost:8000/api/users/test_user/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer dummy-token" \
  -d '{
    "title": "Persistence Test Task",
    "description": "This task is created to test persistence",
    "priority": "medium"
  }' 2>/dev/null)

TASK_ID=$(echo $TASK_RESPONSE | python -c "import sys, json; print(json.load(sys.stdin).get('id', ''))" 2>/dev/null)

if [ ! -z "$TASK_ID" ] && [ "$TASK_ID" != "" ]; then
    echo "Task created successfully with ID: $TASK_ID"

    # Verify the task exists
    echo "Verifying task exists..."
    GET_RESPONSE=$(curl -s -X GET http://localhost:8000/api/users/test_user/tasks/$TASK_ID \
      -H "Authorization: Bearer dummy-token" 2>/dev/null)

    if echo $GET_RESPONSE | grep -q "Persistence Test Task"; then
        echo "✓ Task verification successful"

        # Restart the backend to test persistence
        echo "Restarting backend to test persistence..."
        if [ ! -z "$BACKEND_PID" ]; then
            kill $BACKEND_PID 2>/dev/null
        fi

        sleep 3  # Wait for server to stop

        cd backend
        nohup uvicorn src.main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
        NEW_BACKEND_PID=$!
        cd ..
        sleep 5  # Wait for server to restart

        # Check if task still exists after restart
        echo "Checking if task still exists after restart..."
        FINAL_RESPONSE=$(curl -s -X GET http://localhost:8000/api/users/test_user/tasks/$TASK_ID \
          -H "Authorization: Bearer dummy-token" 2>/dev/null)

        if echo $FINAL_RESPONSE | grep -q "Persistence Test Task"; then
            echo "✓ Persistence test PASSED - Task survived server restart!"
        else
            echo "✗ Persistence test FAILED - Task did not survive server restart"
        fi

        # Cleanup - delete the test task
        curl -X DELETE http://localhost:8000/api/users/test_user/tasks/$TASK_ID \
          -H "Authorization: Bearer dummy-token" 2>/dev/null
        echo "Cleanup completed - test task deleted"

    else
        echo "✗ Task verification failed - unable to retrieve created task"
    fi
else
    echo "✗ Failed to create test task"
    echo "Response was: $TASK_RESPONSE"
fi

# Kill the backend if we started it
if [ ! -z "$NEW_BACKEND_PID" ]; then
    kill $NEW_BACKEND_PID 2>/dev/null
elif [ ! -z "$BACKEND_PID" ]; then
    kill $BACKEND_PID 2>/dev/null
fi

echo "Persistence verification test completed."