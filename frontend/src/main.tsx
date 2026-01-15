/**
 * Application Entry Point (Frontend)
 * ----------------------------------
 * Sets up the React DOM root and wraps the app in the React Query Provider
 * for global server-state management.
 */

import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import './index.css' // Assuming tailwind directives will be here later

// Create a client for React Query
const queryClient = new QueryClient()

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </React.StrictMode>,
)