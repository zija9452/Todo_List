/**
 * API Client for the Todo Application
 * Handles all API calls to the backend with proper authentication
 */

// Define the base URL for the API
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

// Define types for our API responses
export interface Task {
  id: number;
  user_id: string;
  title: string;
  description?: string;
  completed: boolean;
  priority?: 'high' | 'medium' | 'low';
  due_date?: string; // ISO string
  created_at: string; // ISO string
  updated_at: string; // ISO string
}

export interface TaskCreateData {
  title: string;
  description?: string;
  priority?: 'high' | 'medium' | 'low';
  due_date?: string; // ISO string
}

export interface TaskUpdateData {
  title?: string;
  description?: string;
  completed?: boolean;
  priority?: 'high' | 'medium' | 'low';
  due_date?: string; // ISO string
}

// Helper function to get the authorization header with JWT token
async function getAuthHeaders(): Promise<{ [key: string]: string }> {
  // In a real app, you'd get this from your auth provider (e.g., Better Auth)
  // This is a placeholder - replace with actual token retrieval
  const token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null;

  return {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {})
  };
}

// Generic API request function
async function apiRequest<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;

  // Add auth headers to the request
  const authHeaders = await getAuthHeaders();
  const config: RequestInit = {
    ...options,
    headers: {
      ...authHeaders,
      ...options.headers,
    },
  };

  try {
    const response = await fetch(url, config);

    // Handle different response statuses
    if (!response.ok) {
      if (response.status === 401) {
        // Unauthorized - redirect to login or clear auth state
        console.error('Unauthorized access - token may be expired');
        // In a real app, you'd redirect to login page or clear auth state
        // router.push('/login'); // Example with Next.js router
      } else if (response.status === 403) {
        // Forbidden - user doesn't have permission
        throw new Error('You do not have permission to perform this action');
      } else if (response.status === 404) {
        // Not found
        throw new Error('Resource not found');
      } else if (response.status === 422) {
        // Validation error
        const errorData = await response.json();
        throw new Error(`Validation error: ${errorData.detail || 'Invalid input'}`);
      } else {
        // Other error
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }
    }

    // For successful responses that have content, parse JSON
    if (response.status !== 204) { // 204 No Content
      return await response.json();
    }

    // For 204 responses, return void-like response
    return {} as T;
  } catch (error) {
    console.error(`API request failed: ${endpoint}`, error);
    throw error;
  }
}

// Task API functions
export const taskApi = {
  /**
   * Get all tasks for a user
   */
  getTasks: async (userId: string, queryParams?: {
    status?: 'all' | 'pending' | 'completed';
    sort?: 'created' | 'title' | 'due_date';
    order?: 'asc' | 'desc'
  }): Promise<Task[]> => {
    let url = `/api/users/${userId}/tasks`;

    if (queryParams) {
      const params = new URLSearchParams();
      if (queryParams.status) params.append('status', queryParams.status);
      if (queryParams.sort) params.append('sort', queryParams.sort);
      if (queryParams.order) params.append('order', queryParams.order);
      url += `?${params.toString()}`;
    }

    const response = await apiRequest<{ tasks: Task[] }>(url);
    return response.tasks;
  },

  /**
   * Get a specific task by ID
   */
  getTask: async (userId: string, taskId: number): Promise<Task> => {
    const response = await apiRequest<Task>(`/api/users/${userId}/tasks/${taskId}`);
    return response;
  },

  /**
   * Create a new task
   */
  createTask: async (userId: string, taskData: TaskCreateData): Promise<Task> => {
    return await apiRequest<Task>(`/api/users/${userId}/tasks`, {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
  },

  /**
   * Update a task
   */
  updateTask: async (userId: string, taskId: number, taskData: TaskUpdateData): Promise<Task> => {
    return await apiRequest<Task>(`/api/users/${userId}/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    });
  },

  /**
   * Delete a task
   */
  deleteTask: async (userId: string, taskId: number): Promise<void> => {
    await apiRequest(`/api/users/${userId}/tasks/${taskId}`, {
      method: 'DELETE',
    });
  },

  /**
   * Update task completion status
   */
  updateTaskCompletion: async (userId: string, taskId: number, completed: boolean): Promise<Task> => {
    const params = new URLSearchParams({ completed: completed.toString() });
    return await apiRequest<Task>(`/api/users/${userId}/tasks/${taskId}/complete?${params.toString()}`, {
      method: 'PATCH',
    });
  },
};

// Export other API groups if needed in the future
// export const userApi = { /* ... */ };
// export const authApi = { /* ... */ };

export default taskApi;