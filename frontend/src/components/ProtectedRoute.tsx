import { Navigate, Outlet } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

interface Props {
  allowedRole: 'admin' | 'professor' | 'responsavel'
}

export function ProtectedRoute({ allowedRole }: Props) {
  const { isAuthenticated, user } = useAuth()

  // Not authenticated at all → go to login
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  // Authenticated but wrong role → redirect to own dashboard
  if (user?.tipo !== allowedRole) {
    return <Navigate to={`/${user?.tipo}`} replace />
  }

  return <Outlet />
}
