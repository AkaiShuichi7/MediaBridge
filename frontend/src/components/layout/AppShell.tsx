import { Suspense } from 'react'
import { Outlet } from 'react-router-dom'
import { Sidebar } from './Sidebar'
import { BottomNav } from './BottomNav'
import { PageHeader } from './PageHeader'

const PageSkeleton = () => (
  <div className="animate-pulse space-y-6 p-6">
    <div className="flex gap-4">
      <div className="h-32 w-full rounded-xl bg-muted/50" />
      <div className="h-32 w-full rounded-xl bg-muted/50" />
      <div className="h-32 w-full rounded-xl bg-muted/50" />
    </div>
    <div className="h-96 rounded-xl bg-muted/50" />
  </div>
)

export function AppShell() {
  return (
    <div className="flex h-screen w-full bg-background text-foreground antialiased selection:bg-primary/20 selection:text-primary">
      <Sidebar />
      <div className="flex flex-1 flex-col overflow-hidden relative">
        <PageHeader />
        <main className="flex-1 overflow-y-auto scroll-smooth">
          <div className="min-h-full w-full">
            <Suspense fallback={<PageSkeleton />}>
              <Outlet />
            </Suspense>
          </div>
        </main>
        <BottomNav />
      </div>
    </div>
  )
}
