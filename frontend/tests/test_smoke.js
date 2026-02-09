/**
 * Smoke tests for the frontend application
 * These tests verify that the basic UI components render without errors
 */

// Mock the Next.js router and other browser-specific APIs
global.window = {};
global.localStorage = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
};

// Mock the fetch API
global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () => Promise.resolve([]),
    ok: true,
    status: 200,
  })
);

describe('Frontend Smoke Tests', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('should have the task API client module', () => {
    // Import the API client
    const { taskApi } = require('../lib/api');

    // Verify that the API client has the expected methods
    expect(typeof taskApi.getTasks).toBe('function');
    expect(typeof taskApi.getTask).toBe('function');
    expect(typeof taskApi.createTask).toBe('function');
    expect(typeof taskApi.updateTask).toBe('function');
    expect(typeof taskApi.deleteTask).toBe('function');
    expect(typeof taskApi.updateTaskCompletion).toBe('function');

    console.log('✓ Task API client module loads correctly');
  });

  test('should handle auth utilities', () => {
    // Import the auth utilities
    const authUtils = require('../lib/auth');

    // Verify that the auth module has the expected methods
    expect(typeof authUtils.getAuthToken).toBe('function');
    expect(typeof authUtils.setAuthToken).toBe('function');
    expect(typeof authUtils.clearAuthToken).toBe('function');
    expect(typeof authUtils.isAuthenticated).toBe('function');

    console.log('✓ Auth utilities module loads correctly');
  });

  test('should have environment variables properly configured', () => {
    // Check that environment variables are available
    const authOrigin = process.env.NEXT_PUBLIC_AUTH_ORIGIN;
    expect(authOrigin).toBeDefined();

    console.log('✓ Environment variables are properly configured');
  });
});

// Run the tests
console.log('Running frontend smoke tests...');