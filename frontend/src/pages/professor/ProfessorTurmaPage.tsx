import { useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { toast } from 'sonner'
import { api } from '../../services/api'
import { TabNav } from '../../components/professor/TabNav'
import { AttendanceToggle } from '../../components/professor/AttendanceToggle'
import { GradeTable } from '../../components/professor/GradeTable'
import { FrequencyTable } from '../../components/professor/FrequencyTable'
import { Modal } from '../../components/admin/Modal'

type Tab = 'chamada' | 'notas' | 'frequencia'

interface Aluno {
  id: number
  nome: string
}

interface PresencaState {
  aluno_id: number
  presente: boolean
}

interface TurmaInfo {
  id: number
  nome: string
  disciplinas: string[]
  num_alunos: number
}

interface Disciplina {
  id: number
  nome: string
}

// Fetch turma info from minhas-turmas list
function useTurmaInfo(turmaId: number) {
  return useQuery<TurmaInfo | null>({
    queryKey: ['turma-info', turmaId],
    queryFn: async () => {
      const list: TurmaInfo[] = await api.get('/professor/minhas-turmas').then((r) => r.data)
      return list.find((t) => t.id === turmaId) ?? null
    },
  })
}

// Fetch alunos for a turma (from admin endpoint — read-only)
function useTurmaAlunos(turmaId: number) {
  return useQuery<Aluno[]>({
    queryKey: ['turma-alunos', turmaId],
    queryFn: () =>
      api.get(`/admin/alunos?turma_id=${turmaId}&limit=200`).then((r) => {
        const result = r.data
        // Support both paginated {items: [...]} and plain array responses
        return Array.isArray(result) ? result : (result.items ?? [])
      }),
  })
}

// Fetch disciplina ids for this professor+turma
function useTurmaDisciplinas(turmaId: number) {
  return useQuery<Disciplina[]>({
    queryKey: ['turma-disciplinas', turmaId],
    queryFn: () =>
      api.get(`/admin/disciplinas?limit=200`).then((r) => {
        const all: Disciplina[] = Array.isArray(r.data) ? r.data : (r.data.items ?? [])
        return all
      }),
  })
}

// Fetch existing chamada for a date
function useChamada(turmaId: number, dateStr: string) {
  return useQuery({
    queryKey: ['chamada', turmaId, dateStr],
    queryFn: () =>
      api.get(`/professor/turmas/${turmaId}/chamada?date=${dateStr}`).then((r) => r.data),
  })
}

// Save chamada mutation
function useSaveChamada(turmaId: number) {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (body: { disciplina_id: number; data: string; presencas: PresencaState[] }) =>
      api.post(`/professor/turmas/${turmaId}/chamada`, body).then((r) => r.data),
    onSuccess: async (_data, variables) => {
      await qc.invalidateQueries({ queryKey: ['chamada', turmaId, variables.data] })
      await qc.invalidateQueries({ queryKey: ['frequencia', turmaId] })
      toast.success('Chamada salva com sucesso.')
    },
    onError: () => toast.error('Erro ao salvar chamada. Tente novamente.'),
  })
}

export default function ProfessorTurmaPage() {
  const { id } = useParams<{ id: string }>()
  const turmaId = Number(id)

  const [activeTab, setActiveTab] = useState<Tab>('chamada')
  const [selectedDate, setSelectedDate] = useState<string>(
    new Date().toISOString().split('T')[0]
  )
  const [presencas, setPresencas] = useState<Record<number, boolean>>({})
  const [selectedDisciplinaId, setSelectedDisciplinaId] = useState<number>(0)
  const [showOverwriteConfirm, setShowOverwriteConfirm] = useState(false)
  const [pendingSave, setPendingSave] = useState<null | { disciplina_id: number; data: string; presencas: PresencaState[] }>(null)

  const { data: turmaInfo } = useTurmaInfo(turmaId)
  const { data: alunos } = useTurmaAlunos(turmaId)
  const { data: allDisciplinas } = useTurmaDisciplinas(turmaId)
  const { data: chamadaData } = useChamada(turmaId, selectedDate)
  const saveChamada = useSaveChamada(turmaId)

  // Derive disciplinas this professor teaches in this turma
  // turmaInfo.disciplinas is a list of disciplina names — we need IDs
  // Fetch the names-to-id mapping from allDisciplinas
  const turmaDisciplinas: Disciplina[] = (allDisciplinas ?? []).filter((d) =>
    (turmaInfo?.disciplinas ?? []).includes(d.nome)
  )

  // Auto-select first disciplina
  const effectiveDisciplinaId =
    selectedDisciplinaId > 0
      ? selectedDisciplinaId
      : (turmaDisciplinas[0]?.id ?? 0)

  // Initialize presencas from chamadaData or default all-presente
  const effectivePresencas: Record<number, boolean> = (() => {
    if (Object.keys(presencas).length > 0) return presencas
    const base: Record<number, boolean> = {}
    // If chamadaData has presencas, use those; otherwise all true
    if (chamadaData?.presencas?.length > 0) {
      for (const p of chamadaData.presencas) {
        base[p.aluno_id] = p.presente
      }
    } else {
      for (const a of alunos ?? []) {
        base[a.id] = true
      }
    }
    return base
  })()

  const handlePresencaChange = (alunoId: number, presente: boolean) => {
    setPresencas((prev) => ({ ...prev, [alunoId]: presente }))
  }

  const handleSaveChamada = () => {
    const payload = {
      disciplina_id: effectiveDisciplinaId,
      data: selectedDate,
      presencas: (alunos ?? []).map((a) => ({
        aluno_id: a.id,
        presente: effectivePresencas[a.id] ?? true,
      })),
    }
    // If chamada already exists for this date, show confirmation
    if (chamadaData?.id) {
      setPendingSave(payload)
      setShowOverwriteConfirm(true)
    } else {
      saveChamada.mutate(payload)
    }
  }

  const handleConfirmOverwrite = () => {
    if (pendingSave) {
      saveChamada.mutate(pendingSave)
      setPendingSave(null)
    }
    setShowOverwriteConfirm(false)
  }

  // Reset presencas when date changes
  const handleDateChange = (newDate: string) => {
    setSelectedDate(newDate)
    setPresencas({})
  }

  return (
    <div className="p-8">
      {/* Breadcrumb */}
      <nav className="flex items-center gap-2 text-sm mb-6">
        <Link to="/professor" className="text-indigo-600 hover:text-indigo-800 font-medium">
          Minhas Turmas
        </Link>
        <span className="text-gray-400">/</span>
        <span className="text-gray-500">{turmaInfo?.nome ?? '...'}</span>
      </nav>

      {/* Tab navigation */}
      <TabNav active={activeTab} onChange={setActiveTab} />

      {/* Tab panels */}
      {activeTab === 'chamada' && (
        <div>
          {/* Date selector */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">Data da chamada</label>
            <input
              type="date"
              value={selectedDate}
              onChange={(e) => handleDateChange(e.target.value)}
              className="border border-gray-300 rounded-md text-sm px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>

          {/* Existing chamada warning */}
          {chamadaData?.id && (
            <div className="bg-yellow-50 border border-yellow-200 rounded-md p-3 mb-4">
              <p className="text-sm text-yellow-800">
                ⚠ Chamada ja registrada nesta data. Editar ira sobrescrever os registros anteriores.
              </p>
            </div>
          )}

          {/* Disciplina selector (if multiple) */}
          {turmaDisciplinas.length > 1 && (
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">Disciplina</label>
              <select
                value={effectiveDisciplinaId}
                onChange={(e) => setSelectedDisciplinaId(Number(e.target.value))}
                className="border border-gray-300 rounded-md text-sm px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                {turmaDisciplinas.map((d) => (
                  <option key={d.id} value={d.id}>
                    {d.nome}
                  </option>
                ))}
              </select>
            </div>
          )}

          {/* Student attendance list */}
          {!alunos || alunos.length === 0 ? (
            <div className="text-center py-12 text-gray-400 text-sm">
              Nenhum aluno matriculado nesta turma.
            </div>
          ) : (
            <div className="divide-y divide-gray-200 border border-gray-200 rounded-lg overflow-hidden">
              {alunos.map((aluno) => (
                <div
                  key={aluno.id}
                  className="flex items-center justify-between px-4 py-3 bg-white hover:bg-gray-50"
                >
                  <span className="text-sm font-medium text-gray-900">{aluno.nome}</span>
                  <AttendanceToggle
                    presente={effectivePresencas[aluno.id] ?? true}
                    onChange={(presente) => handlePresencaChange(aluno.id, presente)}
                  />
                </div>
              ))}
            </div>
          )}

          <div className="mt-4 flex justify-end">
            <button
              onClick={handleSaveChamada}
              disabled={saveChamada.isPending || effectiveDisciplinaId === 0}
              className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md hover:bg-indigo-700 disabled:opacity-50"
            >
              {saveChamada.isPending ? 'Salvando...' : 'Salvar chamada'}
            </button>
          </div>
        </div>
      )}

      {activeTab === 'notas' && (
        <div>
          {/* Disciplina selector for notas (always show if multiple) */}
          {turmaDisciplinas.length > 1 && (
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">Disciplina</label>
              <select
                value={effectiveDisciplinaId}
                onChange={(e) => setSelectedDisciplinaId(Number(e.target.value))}
                className="border border-gray-300 rounded-md text-sm px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                {turmaDisciplinas.map((d) => (
                  <option key={d.id} value={d.id}>
                    {d.nome}
                  </option>
                ))}
              </select>
            </div>
          )}
          {effectiveDisciplinaId > 0 && (
            <GradeTable turmaId={turmaId} disciplinaId={effectiveDisciplinaId} />
          )}
        </div>
      )}

      {activeTab === 'frequencia' && <FrequencyTable turmaId={turmaId} />}

      {/* Overwrite confirmation */}
      <Modal
        open={showOverwriteConfirm}
        title="Sobrescrever chamada"
        onClose={() => setShowOverwriteConfirm(false)}
      >
        <p className="text-sm text-gray-700 mb-6">
          Esta data ja possui chamada registrada. Deseja sobrescrever?
        </p>
        <div className="flex justify-end gap-3">
          <button
            onClick={() => setShowOverwriteConfirm(false)}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
          >
            Cancelar
          </button>
          <button
            onClick={handleConfirmOverwrite}
            className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md hover:bg-indigo-700"
          >
            Sobrescrever
          </button>
        </div>
      </Modal>
    </div>
  )
}
