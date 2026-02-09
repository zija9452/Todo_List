'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import './globals.css';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();

  useEffect(() => {
    // Listen for unhandled errors and redirect to login if it's a 401 error
    const handleError = (event: ErrorEvent) => {
      // Check if the error message contains unauthorized or 401
      if (event.error?.message?.includes('401') || event.error?.message?.toLowerCase().includes('unauthorized')) {
        // Redirect to login page
        router.push('/login');
      }
    };

    // Add error listener
    window.addEventListener('error', handleError);

    // Clean up
    return () => {
      window.removeEventListener('error', handleError);
    };
  }, [router]);

  return (
    <html lang="en">
      <body className="antialiased">
        <div className="min-h-screen bg-gray-50">
          {/* Navigation Bar */}
          <nav className="bg-white shadow">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="flex justify-between h-16">
                <div className="flex">
                  <div className="flex-shrink-0 flex items-center">
                    <span className="text-xl font-bold text-indigo-600">Todo App</span>
                  </div>
                  <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                    <a href="/dashboard" className="border-indigo-500 text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                      Dashboard
                    </a>
                    <a href="/tasks/new" className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                      New Task
                    </a>
                  </div>
                </div>
                <div className="flex items-center">
                  <div className="ml-3 relative">
                    <div className="flex items-center space-x-4">
                      <button
                        onClick={() => {
                          // In a real app, this would trigger logout via Better Auth
                          // For now, clearing token and redirecting
                          if (typeof window !== 'undefined') {
                            localStorage.removeItem('auth_token');
                          }
                          router.push('/login');
                        }}
                        className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-md text-sm font-medium"
                      >
                        Logout
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </nav>

          {/* Main Content */}
          <main>
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}