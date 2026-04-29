interface DisciplinaBoletimRow {
  status: 'aprovado' | 'reprovado' | 'em_andamento'
}

interface SummaryCardProps {
  rows: DisciplinaBoletimRow[]
}

export function SummaryCard({ rows }: SummaryCardProps) {
  const reprovadoCount = rows.filter((r) => r.status === 'reprovado').length
  const emAndamentoCount = rows.filter((r) => r.status === 'em_andamento').length

  if (reprovadoCount > 0) {
    return (
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 mb-6 flex items-start gap-3">
        <svg className="h-6 w-6 text-yellow-600 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <div>
          <p className="text-xl font-semibold text-yellow-800">{reprovadoCount} disciplina(s) em risco de reprovação</p>
          <p className="text-sm text-yellow-700 mt-1">Verifique as disciplinas destacadas abaixo. Frequência abaixo de 75% ou média inferior a 5,0.</p>
        </div>
      </div>
    )
  }

  if (emAndamentoCount > 0) {
    return (
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-6 flex items-start gap-3">
        <svg className="h-6 w-6 text-blue-600 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <div>
          <p className="text-xl font-semibold text-blue-800">Ano letivo em andamento</p>
          <p className="text-sm text-blue-700 mt-1">O resultado final será exibido após o lançamento de todos os bimestres.</p>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-green-50 border border-green-200 rounded-lg p-6 mb-6 flex items-start gap-3">
      <svg className="h-6 w-6 text-green-600 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <div>
        <p className="text-xl font-semibold text-green-800">Aprovado em todas as disciplinas</p>
        <p className="text-sm text-green-700 mt-1">Média e frequência estão dentro dos limites exigidos.</p>
      </div>
    </div>
  )
}
