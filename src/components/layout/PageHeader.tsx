import { useLocation } from 'react-router-dom'

const PAGE_TITLES: Record<string, string> = {
  '/': '仪表盘',
  '/tasks': '任务管理',
  '/records': '整理记录',
  '/settings': '系统设置'
}

export function PageHeader() {
  const location = useLocation()
  const title = PAGE_TITLES[location.pathname] ?? 'MediaBridge'

  return (
    <header className="lg:hidden sticky top-0 z-10 flex h-28 shrink-0 items-center border-b border-border bg-card/80 backdrop-blur-lg px-4 pt-[env(safe-area-inset-top)] transition-all">
      <div className="flex items-center gap-3">
        <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-linear-to-br from-primary to-primary/80 text-primary-foreground text-xs font-bold shadow-sm">
          MB
        </div>
        <h1 className="text-base font-semibold tracking-tight text-foreground">{title}</h1>
      </div>
    </header>
  )
}
