import { lazy } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClientProvider } from '@tanstack/react-query'
import { Toaster } from 'sonner'
import { queryClient } from '@/lib/query-client'
import { AppShell } from '@/components/layout'
import { ErrorBoundary } from '@/components/ErrorBoundary'
import { AuthProvider, useAuth } from '@/auth/AuthProvider'

const Dashboard = lazy(() => import('@/pages/Dashboard'))
const Tasks = lazy(() => import('@/pages/Tasks'))
const Records = lazy(() => import('@/pages/Records'))
const Settings = lazy(() => import('@/pages/Settings'))
const Login = lazy(() => import('@/pages/Login'))

function AppRoutes() {
  const { user, loading } = useAuth()
  if (loading) return <div className="grid min-h-screen place-items-center text-muted-foreground">正在验证登录状态…</div>
  if (!user) return <Login />
  return <Routes>
    <Route path="/" element={<AppShell />}>
      <Route index element={<Dashboard />} />
      <Route path="tasks" element={<Tasks />} />
      <Route path="records" element={<Records />} />
      <Route path="settings" element={<Settings />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Route>
  </Routes>
}

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
          <AuthProvider><AppRoutes /></AuthProvider>
        </BrowserRouter>
      </ErrorBoundary>
    </QueryClientProvider>
  )
}

export default App
