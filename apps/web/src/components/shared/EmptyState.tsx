import { type LucideIcon, InboxIcon } from 'lucide-react'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'

interface EmptyStateProps {
  icon?: LucideIcon
  title: string
  description?: string
  actionLabel?: string
  onAction?: () => void
  className?: string
}

export function EmptyState({ 
  icon: Icon = InboxIcon, 
  title, 
  description, 
  actionLabel, 
  onAction, 
  className 
}: EmptyStateProps) {
  return (
    <div className={cn('flex flex-col items-center justify-center py-16 text-center animate-in fade-in-50 zoom-in-95 duration-500', className)}>
      <div className="flex h-20 w-20 items-center justify-center rounded-3xl bg-muted/50 mb-6 ring-1 ring-border/50">
        <Icon className="h-10 w-10 text-muted-foreground/60" strokeWidth={1.5} />
      </div>
      <h3 className="text-lg font-semibold text-foreground tracking-tight">{title}</h3>
      {description && (
        <p className="mt-2 text-sm text-muted-foreground max-w-sm leading-relaxed">
          {description}
        </p>
      )}
      {actionLabel && onAction && (
        <Button onClick={onAction} className="mt-8" variant="default" size="default">
          {actionLabel}
        </Button>
      )}
    </div>
  )
}
