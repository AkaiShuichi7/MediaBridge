import { createContext, useContext, useEffect, useState, type ReactNode } from 'react'
import { api } from '@/lib/api'

type User = { id: number; username: string; role: string }
type AuthContextValue = {
  user: User | null
  loading: boolean
  login: (username: string, password: string) => Promise<void>
  logout: () => Promise<void>
}

const AuthContext = createContext<AuthContextValue | null>(null)

function applyCsrfToken(token?: string) {
  if (token) api.defaults.headers.common['X-CSRF-Token'] = token
  else delete api.defaults.headers.common['X-CSRF-Token']
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/api/auth/me')
      .then(({ data }) => {
        setUser(data.data)
        applyCsrfToken(data.data.csrf_token)
      })
      .catch(() => applyCsrfToken())
      .finally(() => setLoading(false))
  }, [])

  async function login(username: string, password: string) {
    const { data } = await api.post('/api/auth/login', { username, password })
    setUser(data.data)
    applyCsrfToken(data.data.csrf_token)
  }

  async function logout() {
    await api.post('/api/auth/logout')
    setUser(null)
    applyCsrfToken()
  }

  return <AuthContext.Provider value={{ user, loading, login, logout }}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth must be used within AuthProvider')
  return context
}
