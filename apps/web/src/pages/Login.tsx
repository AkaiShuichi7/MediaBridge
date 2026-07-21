import { useState, type FormEvent } from 'react'
import { LockKeyhole } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { useAuth } from '@/auth/AuthProvider'

export default function Login() {
  const { login } = useAuth()
  const [username, setUsername] = useState('admin')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  async function submit(event: FormEvent) {
    event.preventDefault()
    setSubmitting(true)
    setError('')
    try {
      await login(username, password)
    } catch {
      setError('用户名或密码错误。')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-muted/40 px-4">
      <Card className="w-full max-w-sm shadow-lg">
        <CardHeader className="space-y-3 text-center">
          <div className="mx-auto flex size-11 items-center justify-center rounded-full bg-primary text-primary-foreground"><LockKeyhole className="size-5" /></div>
          <CardTitle>登录 MediaBridge</CardTitle>
          <CardDescription>请使用管理员账户继续。</CardDescription>
        </CardHeader>
        <CardContent>
          <form className="space-y-4" onSubmit={submit}>
            <div className="space-y-2"><Label htmlFor="username">用户名</Label><Input id="username" value={username} onChange={(event) => setUsername(event.target.value)} autoComplete="username" required /></div>
            <div className="space-y-2"><Label htmlFor="password">密码</Label><Input id="password" type="password" value={password} onChange={(event) => setPassword(event.target.value)} autoComplete="current-password" required /></div>
            {error && <p className="text-sm text-destructive">{error}</p>}
            <Button className="w-full" type="submit" disabled={submitting}>{submitting ? '正在登录…' : '登录'}</Button>
          </form>
        </CardContent>
      </Card>
    </main>
  )
}
