import { NavLink } from 'react-router-dom'
import { useAuth } from '../../contexts/AuthContext'
import { useNavigate } from 'react-router-dom'

const navItems = [
  { to: '/admin', label: 'Dashboard', end: true },
  { to: '/admin/alunos', label: 'Alunos' },
  { to: '/admin/turmas', label: 'Turmas' },
  { to: '/admin/disciplinas', label: 'Disciplinas' },
  { to: '/admin/professores', label: 'Professores' },
  { to: '/admin/responsaveis', label: 'Responsáveis' },
]

export default function Sidebar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login', { replace: true })
  }

  return (
    <aside className="w-56 bg-gray-900 text-white flex flex-col flex-shrink-0">
      <div className="px-4 py-5 border-b border-gray-700">
        <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Sistema Escolar</p>
        <p className="text-sm text-white mt-1 font-medium">Painel Admin</p>
      </div>

      <nav className="flex-1 p-3 space-y-1 overflow-y-auto">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.end}
            className={({ isActive }) =>
              `block px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                isActive
                  ? 'bg-indigo-600 text-white'
                  : 'text-gray-300 hover:bg-gray-700 hover:text-white'
              }`
            }
          >
            {item.label}
          </NavLink>
        ))}
      </nav>

      <div className="p-4 border-t border-gray-700">
        <p className="text-xs text-gray-400 truncate">{user?.nome}</p>
        <button
          onClick={handleLogout}
          className="mt-2 w-full text-left text-xs text-gray-400 hover:text-white transition-colors"
        >
          Sair
        </button>
      </div>
    </aside>
  )
}
