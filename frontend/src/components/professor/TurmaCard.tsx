interface TurmaCardProps {
  turma: {
    id: number
    nome: string
    disciplinas: string[]
    num_alunos: number
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
    </div>
  )
}
