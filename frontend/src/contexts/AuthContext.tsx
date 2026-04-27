import { createContext, useContext, useEffect, useState, useMemo } from 'react'

export interface AuthUser {
  id: number
  email: string
  tipo: 'admin' | 'professor' | 'responsavel'
  nome: string
}

interface AuthContextValue {
  user: AuthUser | null
  token: string | null
  login: (token: string, user: AuthUser) => void
  logout: () => void
  isAuthenticated: boolean
  updateToken: (newToken: string) => void
}

export const AuthContext = createContext<AuthContextValue | null>(null)

// Module-level ref for access outside React component tree (e.g., axios interceptors)
export const authContextRef: { current: AuthContextValue | null } = { current: null }

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(() => {
    const stored = localStorage.getItem('user')
    try {
      return stored ? (JSON.parse(stored) as AuthUser) : null
    } catch {
      return null
    }
  })

  const [token, setToken] = useState<string | null>(() => localStorage.getItem('token'))

  const login = (newToken: string, newUser: AuthUser) => {
    setToken(newToken)
    setUser(newUser)
    localStorage.setItem('token', newToken)
    localStorage.setItem('user', JSON.stringify(newUser))
  }

  const logout = () => {
    setToken(null)
    setUser(null)
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  const updateToken = (newToken: string) => {
    setToken(newToken)
    localStorage.setItem('token', newToken)
  }

  const isAuthenticated = token !== null && user !== null

  const contextValue = useMemo<AuthContextValue>(
    () => ({
      user,
      token,
      login,
      logout,
      isAuthenticated,
      updateToken,
    }),
    [user, token, isAuthenticated],
  )

  // Sync ref for non-React consumers (axios interceptors)
  useEffect(() => {
    authContextRef.current = contextValue
  }, [contextValue])

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
