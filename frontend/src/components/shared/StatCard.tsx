import { type LucideIcon } from 'lucide-react'
import { Card, CardContent } from '@/components/ui/card'
import { cn } from '@/lib/utils'

interface StatCardProps {
  title: string
  value: string | number
  icon: LucideIcon
  description?: string
  iconClassName?: string
  className?: string
}

export function StatCard({ 
  title, 
  value, 
  icon: Icon, 
  description, 
  iconClassName, 
  className 
}: StatCardProps) {
  return (
    <Card className={cn('overflow-hidden transition-all hover:shadow-md border-border/60 bg-card/50 backdrop-blur-sm', className)}>
      <CardContent className="p-6">
        <div className="flex items-start justify-between gap-4">
          <div className="space-y-2">
            <p className="text-xs font-semibold text-muted-foreground/80 uppercase tracking-wider">{title}</p>
            <div className="flex items-baseline gap-2">
              <h3 className="text-3xl font-bold text-foreground tracking-tight tabular-nums">{value}</h3>
            </div>
            {description && <p className="text-xs text-muted-foreground font-medium">{description}</p>}
          </div>
          <div className={cn(
            'flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-2xl bg-primary/10 transition-colors', 
            iconClassName
          )}>
            <Icon className="h-6 w-6 text-primary" strokeWidth={2} />
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
