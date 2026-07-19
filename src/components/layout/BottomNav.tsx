import { NavLink } from 'react-router-dom'
import { LayoutDashboard, ListTodo, FileCheck2, Settings } from 'lucide-react'
import { cn } from '@/lib/utils'

const navItems = [
  { to: '/', icon: LayoutDashboard, label: '仪表盘', end: true },
  { to: '/tasks', icon: ListTodo, label: '任务', end: false },
  { to: '/records', icon: FileCheck2, label: '记录', end: false },
  { to: '/settings', icon: Settings, label: '设置', end: false },
]

export function BottomNav() {
  return (
    <nav className="lg:hidden flex-shrink-0 border-t border-border bg-card/80 backdrop-blur-lg pb-[calc(0.5rem+env(safe-area-inset-bottom))]">
      <div className="flex justify-around p-1">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.end}
            className={({ isActive }) =>
              cn(
                'flex flex-1 flex-col items-center gap-1 rounded-xl py-2 text-[10px] font-medium transition-colors active:scale-95',
                isActive
                  ? 'text-primary'
                  : 'text-muted-foreground hover:text-foreground hover:bg-accent/50'
              )
            }
          >
            <item.icon className="h-5 w-5" />
            <span>{item.label}</span>
          </NavLink>
        ))}
      </div>
    </nav>
  )
}
