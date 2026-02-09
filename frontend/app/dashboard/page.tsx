'use client';

import { useState, useEffect } from 'react';
import { Task, taskApi } from '../../lib/api';

const DashboardPage = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // For demo purposes, using a hardcoded user ID
  // In a real app, this would come from the authenticated user context
  const userId = 'user123';

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        setLoading(true);
        const tasksData = await taskApi.getTasks(userId);
        setTasks(tasksData);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch tasks');
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
  }, []);

  if (loading) {
    return <div className="flex justify-center items-center h-screen">Loading tasks...</div>;
  }

  if (error) {
    return <div className="text-red-500 p-4">Error: {error}</div>;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">My Tasks</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {tasks.map((task) => (
          <div
            key={task.id}
            className={`border rounded-lg p-4 shadow-md ${
              task.completed ? 'bg-green-50 border-green-200' : 'bg-white'
            }`}
          >
            <h2 className="text-xl font-semibold mb-2">{task.title}</h2>
            {task.description && (
              <p className="text-gray-600 mb-2">{task.description}</p>
            )}
            <div className="flex justify-between items-center mt-4">
              <span className={`px-2 py-1 rounded-full text-xs ${
                task.priority === 'high' ? 'bg-red-100 text-red-800' :
                task.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                'bg-green-100 text-green-800'
              }`}>
                {task.priority || 'None'}
              </span>
              <span className={`px-2 py-1 rounded-full text-xs ${
                task.completed ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
              }`}>
                {task.completed ? 'Completed' : 'Pending'}
              </span>
            </div>
            {task.due_date && (
              <p className="text-sm text-gray-500 mt-2">
                Due: {new Date(task.due_date).toLocaleDateString()}
              </p>
            )}
            <div className="mt-4 flex space-x-2">
              <button
                onClick={() => handleToggleCompletion(task)}
                className={`px-3 py-1 rounded ${
                  task.completed
                    ? 'bg-gray-200 hover:bg-gray-300 text-gray-800'
                    : 'bg-blue-500 hover:bg-blue-600 text-white'
                }`}
              >
                {task.completed ? 'Undo' : 'Complete'}
              </button>
              <button
                onClick={() => handleDeleteTask(task.id)}
                className="px-3 py-1 bg-red-500 hover:bg-red-600 text-white rounded"
              >
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>

      {tasks.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-500 text-lg">No tasks yet. Add your first task!</p>
        </div>
      )}
    </div>
  );

  async function handleToggleCompletion(task: Task) {
    try {
      const updatedTask = await taskApi.updateTaskCompletion(userId, task.id, !task.completed);
      setTasks(tasks.map(t => t.id === task.id ? updatedTask : t));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update task');
    }
  }

  async function handleDeleteTask(taskId: number) {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await taskApi.deleteTask(userId, taskId);
        setTasks(tasks.filter(t => t.id !== taskId));
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to delete task');
      }
    }
  }
};

export default DashboardPage;