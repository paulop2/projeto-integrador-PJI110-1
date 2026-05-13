import { Outlet, Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { UserMenu } from './UserMenu'

export default function AppLayout() {
  const { user } = useAuth()

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <a
        href="#conteudo-principal"
        className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-[60] focus:rounded-md focus:bg-white focus:px-3 focus:py-2 focus:text-sm focus:font-medium focus:text-indigo-700 focus:shadow"
      >
        Ir para o conteúdo principal
      </a>
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          {/* Logo */}
          <Link
            to={`/${user?.tipo ?? ''}`}
            className="text-xl font-bold text-indigo-600 hover:text-indigo-700 transition-colors"
          >
            Sistema Escolar
          </Link>

          {/* User menu */}
          <UserMenu />
        </div>
      </header>

      {/* Main content */}
      <main id="conteudo-principal" className="flex-1 pt-16">
        <Outlet />
      </main>
    </div>
  )
}
