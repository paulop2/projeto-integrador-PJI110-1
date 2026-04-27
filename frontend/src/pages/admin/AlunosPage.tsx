import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient, keepPreviousData } from '@tanstack/react-query'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { toast } from 'sonner'
import { api } from '../../services/api'
import { EntityTable } from '../../components/admin/EntityTable'
import { Modal } from '../../components/admin/Modal'
import { ConfirmDialog } from '../../components/admin/ConfirmDialog'

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------
interface AlunoOut {
  id: number
  matricula: string | null
  nome: string
  data_nascimento: string | null
  turma_id: number | null
  turma_nome: string | null
  responsavel_id: number | null
  responsavel_nome: string | null
  ativo: boolean
}

// ---------------------------------------------------------------------------
// Zod schema
// ---------------------------------------------------------------------------
const alunoSchema = z.object({
  nome: z.string().min(1, 'Nome é obrigatório'),
  data_nascimento: z.string().nullable().optional(),
  turma_id: z.number().int().nullable().optional(),
  responsavel_id: z.number().int().nullable().optional(),
})
type AlunoFormData = z.infer<typeof alunoSchema>

// ---------------------------------------------------------------------------
// API hooks
// ---------------------------------------------------------------------------
function useAlunos(page: number, search: string) {
  return useQuery({
    queryKey: ['alunos', { page, search }],
    queryFn: () =>
      api.get('/admin/alunos', { params: { page, search } }).then((r) => r.data),
    placeholderData: keepPreviousData,
  })
}

function useTurmasForSelect() {
  return useQuery({
    queryKey: ['turmas-select'],
    queryFn: () => api.get('/admin/turmas', { params: { page: 1, search: '' } }).then((r) => r.data.items),
  })
}

function useResponsaveisForSelect() {
  return useQuery({
    queryKey: ['responsaveis-select'],
    queryFn: () =>
      api.get('/admin/responsaveis', { params: { page: 1, per_page: 100 } }).then((r) => r.data.items),
  })
}

function useCreateAluno() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (body: AlunoFormData) => api.post('/admin/alunos', body).then((r) => r.data),
    onSuccess: async () => {
      await qc.invalidateQueries({ queryKey: ['alunos'] })
      toast.success('Aluno criado com sucesso')
    },
    onError: () => toast.error('Erro ao criar aluno'),
  })
}

function useUpdateAluno() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ id, body }: { id: number; body: AlunoFormData }) =>
      api.put(`/admin/alunos/${id}`, body).then((r) => r.data),
    onSuccess: async () => {
      await qc.invalidateQueries({ queryKey: ['alunos'] })
      toast.success('Aluno atualizado com sucesso')
    },
    onError: () => toast.error('Erro ao atualizar aluno'),
  })
}

function useDeactivateAluno() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (id: number) => api.post(`/admin/alunos/${id}/deactivate`).then((r) => r.data),
    onSuccess: async () => {
      await qc.invalidateQueries({ queryKey: ['alunos'] })
      toast.success('Aluno desativado')
    },
    onError: () => toast.error('Erro ao desativar aluno'),
  })
}

// ---------------------------------------------------------------------------
// Modal form component
// ---------------------------------------------------------------------------
interface AlunoModalProps {
  open: boolean
  onClose: () => void
  initial?: AlunoOut | null
}

function AlunoModal({ open, onClose, initial }: AlunoModalProps) {
  const { data: turmasData } = useTurmasForSelect()
  const { data: responsaveisData } = useResponsaveisForSelect()
  const createMutation = useCreateAluno()
  const updateMutation = useUpdateAluno()
  const isEdit = !!initial

  const { register, handleSubmit, reset, formState: { errors } } = useForm<AlunoFormData>({
    resolver: zodResolver(alunoSchema),
    defaultValues: { nome: '', data_nascimento: null, turma_id: null, responsavel_id: null },
  })

  useEffect(() => {
    reset(
      initial
        ? {
            nome: initial.nome,
            data_nascimento: initial.data_nascimento ?? null,
            turma_id: initial.turma_id ?? null,
            responsavel_id: initial.responsavel_id ?? null,
          }
        : { nome: '', data_nascimento: null, turma_id: null, responsavel_id: null }
    )
  }, [initial, reset, open])

  const onSubmit = (data: AlunoFormData) => {
    if (isEdit && initial) {
      updateMutation.mutate({ id: initial.id, body: data }, { onSuccess: onClose })
    } else {
      createMutation.mutate(data, { onSuccess: onClose })
    }
  }

  const isPending = createMutation.isPending || updateMutation.isPending

  return (
    <Modal open={open} title={isEdit ? 'Editar Aluno' : 'Novo Aluno'} onClose={onClose}>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Nome *</label>
          <input
            {...register('nome')}
            className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            placeholder="Nome completo do aluno"
          />
          {errors.nome && <p className="mt-1 text-xs text-red-600">{errors.nome.message}</p>}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Data de Nascimento</label>
          <input
            {...register('data_nascimento')}
            type="date"
            className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Turma</label>
          <select
            {...register('turma_id', { setValueAs: (v) => (v === '' ? null : Number(v)) })}
            className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="">Sem turma</option>
            {(turmasData ?? []).map((t: { id: number; nome: string }) => (
              <option key={t.id} value={t.id}>{t.nome}</option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Responsável</label>
          <select
            {...register('responsavel_id', { setValueAs: (v) => (v === '' ? null : Number(v)) })}
            className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="">Sem responsável</option>
            {(responsaveisData ?? []).map((r: { id: number; nome: string }) => (
              <option key={r.id} value={r.id}>{r.nome}</option>
            ))}
          </select>
        </div>

        <div className="flex justify-end gap-3 pt-2">
          <button
            type="button"
            onClick={onClose}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
          >
            Cancelar
          </button>
          <button
            type="submit"
            disabled={isPending}
            className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md hover:bg-indigo-700 disabled:opacity-50"
          >
            {isPending ? 'Salvando...' : 'Salvar'}
          </button>
        </div>
      </form>
    </Modal>
  )
}

// ---------------------------------------------------------------------------
// Page
// ---------------------------------------------------------------------------
const COLUMNS = [
  { key: 'nome', label: 'Nome' },
  { key: 'matricula', label: 'Matrícula' },
  { key: 'turma_nome', label: 'Turma' },
  { key: 'ativo', label: 'Status' },
]

export default function AlunosPage() {
  const [page, setPage] = useState(1)
  const [search, setSearch] = useState('')
  const [modalOpen, setModalOpen] = useState(false)
  const [selectedAluno, setSelectedAluno] = useState<AlunoOut | null>(null)
  const [confirmOpen, setConfirmOpen] = useState(false)
  const [toDeactivate, setToDeactivate] = useState<AlunoOut | null>(null)

  const { data, isLoading } = useAlunos(page, search)
  const deactivateMutation = useDeactivateAluno()

  const openCreate = () => { setSelectedAluno(null); setModalOpen(true) }
  const openEdit = (row: Record<string, unknown>) => { setSelectedAluno(row as unknown as AlunoOut); setModalOpen(true) }
  const openDeactivate = (row: Record<string, unknown>) => { setToDeactivate(row as unknown as AlunoOut); setConfirmOpen(true) }

  const handleDeactivate = () => {
    if (!toDeactivate) return
    deactivateMutation.mutate(toDeactivate.id, {
      onSuccess: () => setConfirmOpen(false),
    })
  }

  return (
    <div className="p-8">
      <h1 className="text-2xl font-semibold text-gray-900 mb-6">Alunos</h1>

      <EntityTable
        columns={COLUMNS}
        rows={(data?.items ?? []) as Record<string, unknown>[]}
        total={data?.total ?? 0}
        page={page}
        perPage={25}
        search={search}
        onPageChange={setPage}
        onSearch={(q) => { setSearch(q); setPage(1) }}
        onEdit={openEdit}
        onDeactivate={openDeactivate}
        isLoading={isLoading}
        onNew={openCreate}
        newLabel="Novo Aluno"
      />

      <AlunoModal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        initial={selectedAluno}
      />

      <ConfirmDialog
        open={confirmOpen}
        entityName={toDeactivate?.nome ?? ''}
        onClose={() => setConfirmOpen(false)}
        onConfirm={handleDeactivate}
        loading={deactivateMutation.isPending}
      />
    </div>
  )
}
