import { useState, useEffect } from 'react'
import { useQuery } from '@tanstack/react-query'
import { api } from '../../services/api'
import { ChildSelector } from '../../components/responsavel/ChildSelector'
import { SummaryCard } from '../../components/responsavel/SummaryCard'
import { BoletimTable } from '../../components/responsavel/BoletimTable'
import { EmptyState } from '../../components/responsavel/EmptyState'

interface FilhoOut {
  id: number
  nome: string
  turma_nome: string | null
}

interface DisciplinaBoletimRow {
  disciplina_id: number
  disciplina_nome: string
  bim1: number | null
  bim2: number | null
  bim3: number | null
  bim4: number | null
  media: number | null
  total_aulas: number
  total_presentes: number
  freq_pct: number | null
  aprovado: boolean
}

function useMeusFilhos() {
  return useQuery<FilhoOut[]>({
    queryKey: ['meus-filhos'],
    queryFn: () => api.get('/responsavel/meus-filhos').then((r) => r.data),
  })
}

function useBoletim(alunoId: number | null) {
  return useQuery<DisciplinaBoletimRow[]>({
    queryKey: ['boletim', alunoId],
    queryFn: () =>
      api.get('/responsavel/boletim', { params: { aluno_id: alunoId } }).then((r) => r.data),
    enabled: alunoId !== null, // do not fire until child is selected
  })
}

export default function ResponsavelBoletimPage() {
  const { data: filhos, isLoading: filhosLoading } = useMeusFilhos()
  const [selectedAlunoId, setSelectedAlunoId] = useState<number | null>(null)

  // Auto-select the first filho when data loads
  useEffect(() => {
    if (filhos && filhos.length > 0 && selectedAlunoId === null) {
      setSelectedAlunoId(filhos[0].id)
    }
  }, [filhos, selectedAlunoId])

  const { data: boletim, isLoading: boletimLoading } = useBoletim(selectedAlunoId)

  // Layout uses pt-16 to clear fixed AppLayout header (h-16), max-w-7xl centered
  return (
    <div className="pt-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

        {filhosLoading ? (
          <div aria-live="polite" className="text-center py-12 text-gray-400 text-sm">
            Carregando boletim...
          </div>
        ) : !filhos || filhos.length === 0 ? (
          <EmptyState variant="no-children" />
        ) : (
          <>
            {/* Page header */}
            <h1 className="text-2xl font-semibold text-gray-900 mb-2">Boletim Escolar</h1>
            <p className="text-sm text-gray-500 mb-6">Ano letivo {new Date().getFullYear()}</p>

            {/* Child selector — only renders when > 1 filho */}
            <ChildSelector
              filhos={filhos}
              selectedId={selectedAlunoId}
              onChange={setSelectedAlunoId}
            />

            {/* Summary card and boletim table */}
            {boletimLoading ? (
              <div aria-live="polite" className="text-center py-12 text-gray-400 text-sm">
                Carregando boletim...
              </div>
            ) : !boletim || boletim.length === 0 ? (
              <EmptyState variant="no-data" />
            ) : (
              <>
                <SummaryCard rows={boletim} />
                <div className="bg-white rounded-lg border border-gray-200 shadow-sm p-4">
                  <BoletimTable rows={boletim} />
                </div>
              </>
            )}
          </>
        )}

      </div>
    </div>
  )
}
