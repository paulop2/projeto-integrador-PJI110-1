import { useAuth } from '../../contexts/AuthContext'

export default function AdminDashboard() {
  const { user } = useAuth()
  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold">Bem-vindo, {user?.nome}!</h1>
      <p className="text-gray-500 mt-2">Painel do administrador — em breve.</p>
    </div>
  )
}
