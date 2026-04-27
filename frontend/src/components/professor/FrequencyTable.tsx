import { useQuery } from '@tanstack/react-query'
import { api } from '../../services/api'

interface FrequenciaRow {
  aluno_id: number
  nome: string
  total_aulas: number
  total_presentes: number
  percentual: number
}

interface FrequencyTableProps {
  turmaId: number
}

export function FrequencyTable({ turmaId }: FrequencyTableProps) {
  const { data: rows, isLoading } = useQuery<FrequenciaRow[]>({
    queryKey: ['frequencia', turmaId],
    queryFn: () => api.get(`/professor/turmas/${turmaId}/frequencia`).then((r) => r.data),
  })

  if (isLoading) {
    return <div className="text-center py-12 text-gray-400 text-sm">Carregando frequencia...</div>
  }

  if (!rows || rows.length === 0) {
    return (
      <div className="text-center py-12 text-gray-400 text-sm">
        Nenhuma chamada registrada para esta turma.
      </div>
    )
  }

  const hasAtRisk = rows.some((r) => r.percentual < 75)

  return (
    <div>
      {hasAtRisk && (
        <div className="bg-blue-50 border border-blue-200 rounded-md p-3 mb-4">
          <p className="text-sm text-blue-800">
            Alunos com frequencia abaixo de 75% estao em risco de reprovacao por falta (LDB art. 24, VI).
          </p>
        </div>
      )}
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Aluno
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Presenca
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Aulas
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {rows.map((row) => {
              const atRisk = row.percentual < 75
              return (
                <tr
                  key={row.aluno_id}
                  className={atRisk ? 'bg-red-50 hover:bg-red-100' : 'hover:bg-gray-50'}
                >
                  <td className="px-4 py-3 text-sm font-medium text-gray-900 whitespace-nowrap">
                    {row.nome}
                  </td>
                  <td className="px-4 py-3 text-sm whitespace-nowrap">
                    <span className={atRisk ? 'text-red-700 font-medium' : 'text-gray-700 font-medium'}>
                      {row.percentual.toFixed(0)}%
                    </span>
                    {atRisk && (
                      <span className="ml-2 inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-red-100 text-red-800">
                        ⚠ Abaixo de 75%
                      </span>
                    )}
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-500 whitespace-nowrap">
                    {row.total_presentes}/{row.total_aulas} aulas
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </div>
  )
}
