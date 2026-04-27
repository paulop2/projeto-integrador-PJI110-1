import { createBrowserRouter, RouterProvider, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import LoginPage from './pages/LoginPage'
import ForgotPasswordPage from './pages/ForgotPasswordPage'
import ResetPasswordPage from './pages/ResetPasswordPage'
import { ProtectedRoute } from './components/ProtectedRoute'
import AppLayout from './components/AppLayout'
import AdminLayout from './components/admin/AdminLayout'
import AdminDashboard from './pages/admin/AdminDashboard'
import AlunosPage from './pages/admin/AlunosPage'
import TurmasPage from './pages/admin/TurmasPage'
import DisciplinasPage from './pages/admin/DisciplinasPage'
import ProfessoresPage from './pages/admin/ProfessoresPage'
import ResponsaveisPage from './pages/admin/ResponsaveisPage'
import ProfessorDashboard from './pages/dashboards/ProfessorDashboard'
import ResponsavelDashboard from './pages/dashboards/ResponsavelDashboard'

function PublicRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, user } = useAuth()
  if (isAuthenticated && user) {
    return <Navigate to={`/${user.tipo}`} replace />
  }
  return <>{children}</>
}

function RootRedirect() {
  const { isAuthenticated, user } = useAuth()
  if (isAuthenticated && user) return <Navigate to={`/${user.tipo}`} replace />
  return <Navigate to="/login" replace />
}

const router = createBrowserRouter([
  {
    path: '/login',
    element: (
      <PublicRoute>
        <LoginPage />
      </PublicRoute>
    ),
  },
  {
    path: '/esqueci-senha',
    element: <ForgotPasswordPage />,
  },
  {
    path: '/redefinir-senha',
    element: <ResetPasswordPage />,
  },
  {
    path: '/admin',
    element: <ProtectedRoute allowedRole="admin" />,
    children: [
      {
        element: <AdminLayout />,
        children: [
          { index: true, element: <AdminDashboard /> },
          { path: 'alunos', element: <AlunosPage /> },
          { path: 'turmas', element: <TurmasPage /> },
          { path: 'disciplinas', element: <DisciplinasPage /> },
          { path: 'professores', element: <ProfessoresPage /> },
          { path: 'responsaveis', element: <ResponsaveisPage /> },
        ],
      },
    ],
  },
  {
    path: '/professor',
    element: <ProtectedRoute allowedRole="professor" />,
    children: [
      {
        element: <AppLayout />,
        children: [{ index: true, element: <ProfessorDashboard /> }],
      },
    ],
  },
  {
    path: '/responsavel',
    element: <ProtectedRoute allowedRole="responsavel" />,
    children: [
      {
        element: <AppLayout />,
        children: [{ index: true, element: <ResponsavelDashboard /> }],
      },
    ],
  },
  {
    path: '/',
    element: <RootRedirect />,
  },
  {
    path: '*',
    element: <Navigate to="/login" replace />,
  },
])

export default function App() {
  return (
    <AuthProvider>
      <RouterProvider router={router} />
    </AuthProvider>
  )
}
