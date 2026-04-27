import { useQuery } from '@tanstack/react-query'
import { api } from '../../services/api'

interface DashboardCounts {
  alunos: number
  turmas: number
  disciplinas: number
  professores: number
  responsaveis: number
}

function useAdminDashboard() {
  return useQuery<DashboardCounts>({
    queryKey: ['admin-dashboard'],
    queryFn: () => api.get('/admin/dashboard').then((r) => r.data),
  })
}

const countCards = [
  { key: 'alunos' as const, label: 'Alunos', color: 'bg-blue-50 text-blue-700 border-blue-200' },
  { key: 'turmas' as const, label: 'Turmas', color: 'bg-green-50 text-green-700 border-green-200' },
  { key: 'disciplinas' as const, label: 'Disciplinas', color: 'bg-purple-50 text-purple-700 border-purple-200' },
  { key: 'professores' as const, label: 'Professores', color: 'bg-yellow-50 text-yellow-700 border-yellow-200' },
  { key: 'responsaveis' as const, label: 'Responsáveis', color: 'bg-pink-50 text-pink-700 border-pink-200' },
]

export default function AdminDashboard() {
  const { data, isLoading, isError } = useAdminDashboard()

  return (
    <div className="p-8">
      <h1 className="text-2xl font-semibold text-gray-900 mb-2">Dashboard</h1>
      <p className="text-sm text-gray-500 mb-8">Visão geral da estrutura escolar</p>

      {isError && (
        <div className="mb-4 p-3 bg-red-50 text-red-700 text-sm rounded-md border border-red-200">
          Erro ao carregar dados. Verifique se o backend está rodando.
        </div>
      )}

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
        {countCards.map(({ key, label, color }) => (
          <div
            key={key}
            className={`rounded-lg border p-4 ${color}`}
          >
            <p className="text-3xl font-bold">
              {isLoading ? '—' : (data?.[key] ?? 0)}
            </p>
            <p className="text-sm font-medium mt-1">{label}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
