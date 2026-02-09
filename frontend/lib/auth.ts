/**
 * Better Auth Configuration for the Todo Application
 * Sets up authentication with JWT token handling
 */

import { createAuthClient } from '@better-auth/client';
import { createAuth } from 'better-auth';

// Get the auth origin from environment variables
const AUTH_ORIGIN = process.env.NEXT_PUBLIC_AUTH_ORIGIN || 'http://localhost:3000';

// Initialize the Better Auth client
export const authClient = createAuthClient({
  baseURL: AUTH_ORIGIN, // The base URL of your backend auth service
  // Additional configuration options can be added here
});

// If we're using a server-side auth setup, we'd initialize it like this:
// export const auth = createAuth({
//   secret: process.env.BETTER_AUTH_SECRET || 'fallback-secret-for-dev',
//   trustHost: true,
//   database: {
//     provider: 'postgresql',
//     url: process.env.DATABASE_URL || '',
//   },
//   plugins: [
//     // Add any required plugins here
//   ]
// });

// For client-side operations, export utility functions
export const getAuthToken = (): string | null => {
  if (typeof window !== 'undefined') {
    // In a real implementation, you would get the token from Better Auth's session
    // For now, using localStorage as a placeholder
    return localStorage.getItem('auth_token');
  }
  return null;
};

export const setAuthToken = (token: string): void => {
  if (typeof window !== 'undefined') {
    // In a real implementation, you would set the token using Better Auth's session
    // For now, using localStorage as a placeholder
    localStorage.setItem('auth_token', token);
  }
};

export const clearAuthToken = (): void => {
  if (typeof window !== 'undefined') {
    // In a real implementation, you would clear the token using Better Auth's session
    // For now, using localStorage as a placeholder
    localStorage.removeItem('auth_token');
  }
};

export const isAuthenticated = (): boolean => {
  const token = getAuthToken();
  // In a real implementation, you would validate the token with Better Auth
  // For now, just checking if a token exists
  return !!token;
};

// Export the auth client for use in components
export default authClient;