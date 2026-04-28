interface TurmaCardProps {
  turma: {
    id: number
    nome: string
    disciplinas: string[]
    num_alunos: number
    media_geral?: number | null
    pct_aprovados?: number | null
  }
  onClick: () => void
}

export function TurmaCard({ turma, onClick }: TurmaCardProps) {
  return (
    <div
      onClick={onClick}
      className="bg-white rounded-lg border border-gray-200 p-4 hover:border-indigo-300 hover:shadow-md transition-all cursor-pointer"
    >
      <h2 className="text-xl font-semibold text-gray-900">{turma.nome}</h2>
      <p className="text-sm text-gray-500 mt-1">{turma.disciplinas.join(', ')}</p>
      <p className="text-sm text-gray-700 mt-2">{turma.num_alunos} alunos</p>
      <div className="flex items-center gap-4 mt-3 pt-3 border-t border-gray-100">
        <div>
          <p className="text-xs text-gray-500">Média geral</p>
          <p className="text-sm font-semibold text-gray-900">
            {turma.media_geral != null ? turma.media_geral.toFixed(1) : '—'}
          </p>
        </div>
        <div>
          <p className="text-xs text-gray-500">% Aprovados</p>
          <p className="text-sm font-semibold text-gray-900">
            {turma.pct_aprovados != null ? `${turma.pct_aprovados.toFixed(0)}%` : '—'}
          </p>
        </div>
      </div>
    </div>
  )
}
