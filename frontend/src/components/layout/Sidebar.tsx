import { NavLink } from 'react-router-dom'
import { LayoutDashboard, ListTodo, FileCheck2, Settings, Activity } from 'lucide-react'
import { cn } from '@/lib/utils'
import { useStatus } from '@/hooks/queries'

const navItems = [
  { to: '/', icon: LayoutDashboard, label: '仪表盘', end: true },
  { to: '/tasks', icon: ListTodo, label: '任务管理', end: false },
  { to: '/records', icon: FileCheck2, label: '整理记录', end: false },
  { to: '/settings', icon: Settings, label: '系统设置', end: false },
]

export function Sidebar() {
  const { data: status } = useStatus()
  
  return (
    <aside className="hidden lg:flex w-64 flex-col border-r border-border bg-card/50 backdrop-blur-xl">
      <div className="flex h-16 items-center gap-3 border-b border-border px-6">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground text-sm font-bold shadow-sm shadow-primary/20">MB</div>
        <span className="text-base font-semibold tracking-tight">MediaBridge</span>
      </div>
      <nav className="flex-1 space-y-1 p-3">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.end}
            className={({ isActive }) =>
              cn(
                'group flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-all duration-200',
                isActive
                  ? 'bg-primary/10 text-primary shadow-sm'
                  : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground hover:translate-x-1'
              )
            }
          >
            {({ isActive }) => (
              <>
                <item.icon className={cn("h-4 w-4 flex-shrink-0 transition-transform duration-200", isActive && "scale-110")} />
                {item.label}
                {isActive && <div className="ml-auto h-1.5 w-1.5 rounded-full bg-primary" />}
              </>
            )}
          </NavLink>
        ))}
      </nav>
      <div className="border-t border-border p-4">
        <div className="flex items-center gap-2 rounded-lg border border-border bg-background/50 p-3 text-xs text-muted-foreground">
          <Activity className={cn("h-3.5 w-3.5", status?.monitor_running && "animate-pulse text-emerald-500")} />
          <span>监控状态：</span>
          <span className={cn('font-medium', status?.monitor_running ? 'text-emerald-500' : 'text-red-500')}>
            {status?.monitor_running ? '运行中' : '已停止'}
          </span>
          {status?.active_tasks ? (
            <span className="ml-auto flex h-5 min-w-[1.25rem] items-center justify-center rounded-full bg-primary/10 px-1.5 text-[10px] font-bold text-primary">
              {status.active_tasks}
            </span>
          ) : null}
        </div>
      </div>
    </aside>
  )
}
