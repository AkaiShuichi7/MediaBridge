import { Badge } from '@/components/ui/badge'
import { TASK_STATUS, ORGANIZE_STATUS } from '@/types/api'
import { cn } from '@/lib/utils'

interface TaskStatusBadgeProps { status: number; className?: string }

export function TaskStatusBadge({ status, className }: TaskStatusBadgeProps) {
  const config: Record<number, { label: string; className: string }> = {
    [TASK_STATUS.PENDING]: { label: '进行中', className: 'bg-blue-500/10 text-blue-500 border-blue-500/20 hover:bg-blue-500/20' },
    [TASK_STATUS.FAILED]: { label: '失败', className: 'bg-red-500/10 text-red-500 border-red-500/20 hover:bg-red-500/20' },
    [TASK_STATUS.COMPLETED]: { label: '完成', className: 'bg-emerald-500/10 text-emerald-500 border-emerald-500/20 hover:bg-emerald-500/20' },
  }
  
  const { label, className: statusClassName } = config[status] || { label: '未知', className: 'bg-gray-500/10 text-gray-500 border-gray-500/20' }

  return (
    <Badge variant="outline" className={cn('text-xs font-medium', statusClassName, className)}>
      {status === TASK_STATUS.PENDING && (
        <span className="mr-1.5 inline-block h-1.5 w-1.5 rounded-full bg-blue-500 animate-pulse" />
      )}
      {label}
    </Badge>
  )
}

interface OrganizeStatusBadgeProps { status: number; className?: string }

export function OrganizeStatusBadge({ status, className }: OrganizeStatusBadgeProps) {
  const config: Record<number, { label: string; className: string }> = {
    [ORGANIZE_STATUS.SUCCESS]: { label: '成功', className: 'bg-emerald-500/10 text-emerald-500 border-emerald-500/20 hover:bg-emerald-500/20' },
    [ORGANIZE_STATUS.FAILED]: { label: '失败', className: 'bg-red-500/10 text-red-500 border-red-500/20 hover:bg-red-500/20' },
  }
  
  const { label, className: statusClassName } = config[status] || { label: '未知', className: 'bg-gray-500/10 text-gray-500 border-gray-500/20' }

  return (
    <Badge variant="outline" className={cn('text-xs font-medium', statusClassName, className)}>
      {label}
    </Badge>
  )
}
