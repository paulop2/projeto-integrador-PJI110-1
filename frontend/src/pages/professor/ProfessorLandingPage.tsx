import { useQuery } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { api } from '../../services/api'
import { TurmaCard } from '../../components/professor/TurmaCard'
import { SkeletonCard } from '../../components/SkeletonCard'

interface Turma {
  id: number
  nome: string
  disciplinas: string[]
  num_alunos: number
  media_geral?: number | null
  pct_aprovados?: number | null
}

function useMinhasTurmas() {
  return useQuery<Turma[]>({
    queryKey: ['minhas-turmas'],
    queryFn: () => api.get('/professor/minhas-turmas').then((r) => r.data),
  })
}

export default function ProfessorLandingPage() {
  const navigate = useNavigate()
  const { data: turmas, isLoading } = useMinhasTurmas()

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold text-gray-900">Minhas Turmas</h1>
      <p className="text-sm text-gray-500 mt-1">
        Selecione uma turma para registrar chamada ou lancar notas
      </p>

      {isLoading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mt-6">
          {[1, 2, 3].map((i) => (
            <SkeletonCard key={i} rows={3} />
          ))}
        </div>
      ) : !turmas || turmas.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-xl font-medium text-gray-900">Nenhuma turma vinculada</p>
          <p className="text-sm text-gray-500 mt-2">
            Entre em contato com a administracao para vincular turmas ao seu perfil.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mt-6">
          {turmas.map((t) => (
            <TurmaCard
              key={t.id}
              turma={t}
              onClick={() => navigate(`/professor/turmas/${t.id}`)}
            />
          ))}
        </div>
      )}
    </div>
  )
}
