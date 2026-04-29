import { useQuery } from '@tanstack/react-query'
import { api } from '../../services/api'
import { StatusBadge } from '../../components/responsavel/StatusBadge'
import { SkeletonTable } from '../../components/SkeletonTable'

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

interface TurmaDesempenho {
  turma_id: number
  turma_nome: string
  num_alunos: number
  media_geral: number | null
  pct_aprovados: number | null
}

interface DashboardDesempenho {
  alunos_em_risco: number
  turmas: TurmaDesempenho[]
}

function useAdminDesempenho() {
  return useQuery<DashboardDesempenho>({
    queryKey: ['admin-desempenho'],
    queryFn: () => api.get('/admin/dashboard/desempenho').then((r) => r.data),
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
  const { data: desempenho, isLoading: desempenhoLoading, isError: desempenhoError } = useAdminDesempenho()

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

      <h2 className="text-lg font-semibold text-gray-900 mt-8 mb-4">Desempenho por Turma</h2>

      {desempenhoError && (
        <div className="mb-4 p-3 bg-red-50 text-red-700 text-sm rounded-md border border-red-200">
          Erro ao carregar desempenho.
        </div>
      )}

      {desempenhoLoading ? (
        <SkeletonTable rows={5} columns={5} />
      ) : desempenho ? (
        <div>
          {desempenho.alunos_em_risco === 0 ? (
            <div className="mb-4 p-4 rounded-lg border bg-green-50 border-green-200 flex items-start gap-3">
              <svg className="w-5 h-5 text-green-600 mt-0.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
              </svg>
              <div>
                <p className="text-sm font-medium text-green-800">Nenhum aluno em risco de reprovação</p>
              </div>
            </div>
          ) : (
            <div className="mb-4 p-4 rounded-lg border bg-yellow-50 border-yellow-200 flex items-start gap-3">
              <svg className="w-5 h-5 text-yellow-600 mt-0.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
              <div>
                <p className="text-sm font-medium text-yellow-800">{desempenho.alunos_em_risco} aluno(s) em risco de reprovação</p>
                <p className="text-xs text-yellow-700 mt-1">Média inferior a 5,0 ou frequência abaixo de 75% em pelo menos uma disciplina.</p>
              </div>
            </div>
          )}

          {desempenho.turmas.length === 0 ? (
            <p className="text-sm text-gray-500">Nenhuma turma cadastrada.</p>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200 border border-gray-200 rounded-lg">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Turma</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Alunos</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Média Geral</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">% Aprovados</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {desempenho.turmas.map((turma) => (
                    <tr key={turma.turma_id}>
                      <td className="px-4 py-3 text-sm text-gray-900">{turma.turma_nome}</td>
                      <td className="px-4 py-3 text-sm text-gray-500">{turma.num_alunos}</td>
                      <td className="px-4 py-3 text-sm text-gray-500">{turma.media_geral?.toFixed(1) ?? '—'}</td>
                      <td className="px-4 py-3 text-sm text-gray-500">{turma.pct_aprovados?.toFixed(0) ?? '—'}%</td>
                      <td className="px-4 py-3">
                        <StatusBadge aprovado={(turma.pct_aprovados ?? 0) >= 60} />
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      ) : null}
    </div>
  )
}
