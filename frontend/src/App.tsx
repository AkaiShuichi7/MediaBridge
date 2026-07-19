import { lazy } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClientProvider } from '@tanstack/react-query'
import { Toaster } from 'sonner'
import { queryClient } from '@/lib/query-client'
import { AppShell } from '@/components/layout'
import { ErrorBoundary } from '@/components/ErrorBoundary'

const Dashboard = lazy(() => import('@/pages/Dashboard'))
const Tasks = lazy(() => import('@/pages/Tasks'))
const Records = lazy(() => import('@/pages/Records'))
const Settings = lazy(() => import('@/pages/Settings'))

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ErrorBoundary>
        <BrowserRouter>
          <Toaster 
            richColors 
            position="top-center" 
            closeButton
          />
          <Routes>
            <Route path="/" element={<AppShell />}>
              <Route index element={<Dashboard />} />
              <Route path="tasks" element={<Tasks />} />
              <Route path="records" element={<Records />} />
              <Route path="settings" element={<Settings />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Route>
          </Routes>
        </BrowserRouter>
      </ErrorBoundary>
    </QueryClientProvider>
  )
}

export default App
