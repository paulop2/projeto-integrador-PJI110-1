import { useQuery } from '@tanstack/react-query'
import { useAuth } from '../../contexts/AuthContext'
import { api } from '../../services/api'

interface DashboardCounts {
  alunos: number
  turmas: number
  disciplinas: number
  professores: number
  responsaveis: number
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

const cardConfig = [
  {
    key: 'alunos' as const,
    label: 'Alunos',
    bg: 'bg-indigo-50',
    text: 'text-indigo-600',
    icon: (
      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
        <circle cx="9" cy="7" r="4" />
        <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
        <path d="M16 3.13a4 4 0 0 1 0 7.75" />
      </svg>
    ),
  },
  {
    key: 'turmas' as const,
    label: 'Turmas',
    bg: 'bg-violet-50',
    text: 'text-violet-600',
    icon: (
      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
        <polyline points="9 22 9 12 15 12 15 22" />
      </svg>
    ),
  },
  {
    key: 'disciplinas' as const,
    label: 'Disciplinas',
    bg: 'bg-sky-50',
    text: 'text-sky-600',
    icon: (
      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
        <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
      </svg>
    ),
  },
  {
    key: 'professores' as const,
    label: 'Professores',
    bg: 'bg-amber-50',
    text: 'text-amber-600',
    icon: (
      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <circle cx="12" cy="8" r="4" />
        <path d="M20 21a8 8 0 1 0-16 0" />
      </svg>
    ),
  },
  {
    key: 'responsaveis' as const,
    label: 'Responsáveis',
    bg: 'bg-emerald-50',
    text: 'text-emerald-600',
    icon: (
      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
        <circle cx="9" cy="7" r="3" />
        <circle cx="15" cy="7" r="3" />
      </svg>
    ),
  },
]

export default function AdminDashboard() {
  const { user } = useAuth()

  const { data: counts, isLoading, isError } = useQuery<DashboardCounts>({
    queryKey: ['admin-dashboard'],
    queryFn: () => api.get('/admin/dashboard').then((r) => r.data),
  })

  const { data: desempenho, isLoading: desempenhoLoading } = useQuery<DashboardDesempenho>({
    queryKey: ['admin-desempenho'],
    queryFn: () => api.get('/admin/dashboard/desempenho').then((r) => r.data),
  })

  const hora = new Date().getHours()
  const saudacao = hora < 12 ? 'Bom dia' : hora < 18 ? 'Boa tarde' : 'Boa noite'
  const primeiroNome = user?.nome?.split(' ')[0] ?? 'Admin'

  return (
    <div className="p-8 max-w-5xl">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">
          {saudacao}, {primeiroNome}
        </h1>
        <p className="text-sm text-gray-500 mt-1">Visão geral da escola para {new Date().getFullYear()}.</p>
      </div>

      {isError && (
        <div className="mb-6 p-3 bg-red-50 text-red-700 text-sm rounded-lg border border-red-200">
          Erro ao carregar dados. Verifique se o backend está rodando.
        </div>
      )}

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 mb-10">
        {cardConfig.map(({ key, label, bg, text, icon }) => (
          <div key={key} className="bg-white rounded-xl border border-gray-200 p-5">
            <div className={`w-9 h-9 rounded-lg flex items-center justify-center mb-3 ${bg} ${text}`}>
              {icon}
            </div>
            <p className="text-2xl font-bold text-gray-900 leading-tight">
              {isLoading
                ? <span className="inline-block w-8 h-6 bg-gray-100 rounded animate-pulse align-middle" />
                : (counts?.[key] ?? 0)}
            </p>
            <p className="text-xs text-gray-500 mt-0.5 font-medium">{label}</p>
          </div>
        ))}
      </div>

      {/* Desempenho */}
      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
          <h2 className="text-sm font-semibold text-gray-900">Desempenho por Turma</h2>
          {desempenho && desempenho.alunos_em_risco > 0 && (
            <span className="inline-flex items-center gap-1.5 text-xs font-semibold text-amber-700 bg-amber-50 border border-amber-200 rounded-full px-2.5 py-1">
              <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
                <line x1="12" y1="9" x2="12" y2="13" />
                <line x1="12" y1="17" x2="12.01" y2="17" />
              </svg>
              {desempenho.alunos_em_risco} em risco
            </span>
          )}
          {desempenho && desempenho.alunos_em_risco === 0 && (
            <span className="inline-flex items-center gap-1.5 text-xs font-semibold text-emerald-700 bg-emerald-50 border border-emerald-200 rounded-full px-2.5 py-1">
              <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
                <polyline points="22 4 12 14.01 9 11.01" />
              </svg>
              Sem alunos em risco
            </span>
          )}
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-gray-50 border-b border-gray-100">
                <th className="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Turma</th>
                <th className="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Alunos</th>
                <th className="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Média Geral</th>
                <th className="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">% Aprovados</th>
                <th className="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Situação</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {desempenhoLoading
                ? [1, 2, 3].map((i) => (
                    <tr key={i}>
                      {[1, 2, 3, 4, 5].map((j) => (
                        <td key={j} className="px-6 py-3">
                          <div className="h-4 bg-gray-100 rounded animate-pulse w-14" />
                        </td>
                      ))}
                    </tr>
                  ))
                : desempenho?.turmas.length === 0
                ? (
                  <tr>
                    <td colSpan={5} className="px-6 py-10 text-center text-gray-400 text-sm">
                      Nenhuma turma com dados de desempenho.
                    </td>
                  </tr>
                )
                : desempenho?.turmas.map((t) => {
                    const pct = t.pct_aprovados ?? null
                    const media = t.media_geral ?? null
                    const ok = pct !== null && pct >= 60
                    return (
                      <tr key={t.turma_id} className="hover:bg-gray-50 transition-colors">
                        <td className="px-6 py-3 font-medium text-gray-900">{t.turma_nome}</td>
                        <td className="px-6 py-3 text-gray-600">{t.num_alunos}</td>
                        <td className="px-6 py-3">
                          {media !== null ? (
                            <span className={`font-semibold ${media >= 5 ? 'text-gray-900' : 'text-red-600'}`}>
                              {media.toFixed(1)}
                            </span>
                          ) : <span className="text-gray-400">—</span>}
                        </td>
                        <td className="px-6 py-3">
                          {pct !== null
                            ? <span className={`font-semibold ${pct >= 60 ? 'text-gray-900' : 'text-red-600'}`}>{pct.toFixed(0)}%</span>
                            : <span className="text-gray-400">—</span>}
                        </td>
                        <td className="px-6 py-3">
                          {pct === null ? (
                            <span className="text-gray-400 text-xs">sem dados</span>
                          ) : ok ? (
                            <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700">
                              Regular
                            </span>
                          ) : (
                            <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-semibold bg-red-50 text-red-700">
                              Atenção
                            </span>
                          )}
                        </td>
                      </tr>
                    )
                  })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
