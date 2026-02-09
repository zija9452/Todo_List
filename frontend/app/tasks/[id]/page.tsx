'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Task, TaskUpdateData, taskApi } from '../../../lib/api';

const TaskDetailPage = () => {
  const params = useParams();
  const router = useRouter();
  const taskId = parseInt(params.id as string, 10);

  const [task, setTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    priority: '',
    due_date: '',
  });
  const [error, setError] = useState<string | null>(null);

  // For demo purposes, using a hardcoded user ID
  // In a real app, this would come from the authenticated user context
  const userId = 'user123';

  useEffect(() => {
    const fetchTask = async () => {
      try {
        setLoading(true);
        const taskData = await taskApi.getTask(userId, taskId);
        setTask(taskData);

        // Set form data to current task values for editing
        setFormData({
          title: taskData.title,
          description: taskData.description || '',
          priority: taskData.priority || '',
          due_date: taskData.due_date || '',
        });
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch task');
      } finally {
        setLoading(false);
      }
    };

    fetchTask();
  }, [taskId]);

  const handleEditClick = () => {
    setEditing(true);
  };

  const handleCancelEdit = () => {
    setEditing(false);
    // Reset form data to original values
    if (task) {
      setFormData({
        title: task.title,
        description: task.description || '',
        priority: task.priority || '',
        due_date: task.due_date || '',
      });
    }
  };

  const handleSaveEdit = async () => {
    if (!task) return;

    try {
      const updateData: TaskUpdateData = {
        title: formData.title || undefined,
        description: formData.description || undefined,
        priority: formData.priority as 'high' | 'medium' | 'low' || undefined,
        due_date: formData.due_date || undefined,
      };

      const updatedTask = await taskApi.updateTask(userId, task.id, updateData);
      setTask(updatedTask);
      setEditing(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update task');
    }
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await taskApi.deleteTask(userId, taskId);
        router.push('/dashboard');
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to delete task');
      }
    }
  };

  const handleToggleCompletion = async () => {
    if (!task) return;

    try {
      const updatedTask = await taskApi.updateTaskCompletion(userId, task.id, !task.completed);
      setTask(updatedTask);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update task completion');
    }
  };

  if (loading) {
    return <div className="flex justify-center items-center h-screen">Loading task...</div>;
  }

  if (error) {
    return <div className="text-red-500 p-4">Error: {error}</div>;
  }

  if (!task) {
    return <div className="text-center py-12">Task not found</div>;
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-2xl">
      <div className="flex justify-between items-start mb-6">
        <h1 className="text-3xl font-bold">Task Details</h1>
        <button
          onClick={() => router.back()}
          className="px-4 py-2 text-sm bg-gray-200 hover:bg-gray-300 rounded-md"
        >
          Back
        </button>
      </div>

      {editing ? (
        <div className="space-y-6">
          <div>
            <label htmlFor="edit-title" className="block text-sm font-medium text-gray-700 mb-1">
              Title *
            </label>
            <input
              type="text"
              id="edit-title"
              value={formData.title}
              onChange={(e) => setFormData({...formData, title: e.target.value})}
              required
              minLength={1}
              maxLength={200}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>

          <div>
            <label htmlFor="edit-description" className="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea
              id="edit-description"
              value={formData.description}
              onChange={(e) => setFormData({...formData, description: e.target.value})}
              rows={4}
              maxLength={1000}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label htmlFor="edit-priority" className="block text-sm font-medium text-gray-700 mb-1">
                Priority
              </label>
              <select
                id="edit-priority"
                value={formData.priority}
                onChange={(e) => setFormData({...formData, priority: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              >
                <option value="">Select priority</option>
                <option value="high">High</option>
                <option value="medium">Medium</option>
                <option value="low">Low</option>
              </select>
            </div>

            <div>
              <label htmlFor="edit-due-date" className="block text-sm font-medium text-gray-700 mb-1">
                Due Date
              </label>
              <input
                type="date"
                id="edit-due-date"
                value={formData.due_date}
                onChange={(e) => setFormData({...formData, due_date: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
          </div>

          <div className="flex space-x-4 pt-4">
            <button
              onClick={handleSaveEdit}
              className="px-6 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-md font-medium"
            >
              Save Changes
            </button>
            <button
              onClick={handleCancelEdit}
              className="px-6 py-2 bg-gray-200 hover:bg-gray-300 rounded-md font-medium"
            >
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <div className="border rounded-lg p-6 bg-white shadow-md">
          <div className="flex justify-between items-start">
            <h2 className="text-2xl font-semibold">{task.title}</h2>
            <div className="flex space-x-2">
              <button
                onClick={handleEditClick}
                className="px-3 py-1 bg-blue-500 hover:bg-blue-600 text-white rounded text-sm"
              >
                Edit
              </button>
              <button
                onClick={handleDelete}
                className="px-3 py-1 bg-red-500 hover:bg-red-600 text-white rounded text-sm"
              >
                Delete
              </button>
            </div>
          </div>

          {task.description && (
            <p className="text-gray-600 mt-3">{task.description}</p>
          )}

          <div className="mt-6 grid grid-cols-2 gap-4">
            <div>
              <h3 className="text-sm font-medium text-gray-500">Status</h3>
              <div className="mt-1">
                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                  task.completed
                    ? 'bg-green-100 text-green-800'
                    : 'bg-yellow-100 text-yellow-800'
                }`}>
                  {task.completed ? 'Completed' : 'Pending'}
                </span>
              </div>
            </div>

            <div>
              <h3 className="text-sm font-medium text-gray-500">Priority</h3>
              <div className="mt-1">
                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                  task.priority === 'high' ? 'bg-red-100 text-red-800' :
                  task.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                  task.priority === 'low' ? 'bg-green-100 text-green-800' :
                  'bg-gray-100 text-gray-800'
                }`}>
                  {task.priority || 'Not set'}
                </span>
              </div>
            </div>

            <div>
              <h3 className="text-sm font-medium text-gray-500">Due Date</h3>
              <div className="mt-1 text-sm text-gray-900">
                {task.due_date ? new Date(task.due_date).toLocaleDateString() : 'Not set'}
              </div>
            </div>

            <div>
              <h3 className="text-sm font-medium text-gray-500">Created</h3>
              <div className="mt-1 text-sm text-gray-900">
                {new Date(task.created_at).toLocaleString()}
              </div>
            </div>
          </div>

          <div className="mt-6 pt-6 border-t">
            <div className="flex space-x-4">
              <button
                onClick={handleToggleCompletion}
                className={`px-4 py-2 rounded-md font-medium ${
                  task.completed
                    ? 'bg-gray-200 hover:bg-gray-300 text-gray-800'
                    : 'bg-green-500 hover:bg-green-600 text-white'
                }`}
              >
                {task.completed ? 'Mark as Pending' : 'Mark as Complete'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TaskDetailPage;