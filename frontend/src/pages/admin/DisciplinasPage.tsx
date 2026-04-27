import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient, keepPreviousData } from '@tanstack/react-query'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { toast } from 'sonner'
import { api } from '../../services/api'
import { EntityTable } from '../../components/admin/EntityTable'
import { Modal } from '../../components/admin/Modal'

interface DisciplinaOut {
  id: number
  nome: string
  carga_horaria: number | null
}

const disciplinaSchema = z.object({
  nome: z.string().min(1, 'Nome é obrigatório'),
  carga_horaria: z.number().int().positive().nullable().optional(),
})
type DisciplinaFormData = z.infer<typeof disciplinaSchema>

function useDisciplinas(page: number, search: string) {
  return useQuery({
    queryKey: ['disciplinas', { page, search }],
    queryFn: () => api.get('/admin/disciplinas', { params: { page, search } }).then((r) => r.data),
    placeholderData: keepPreviousData,
  })
}

function useCreateDisciplina() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (body: DisciplinaFormData) => api.post('/admin/disciplinas', body).then((r) => r.data),
    onSuccess: async () => { await qc.invalidateQueries({ queryKey: ['disciplinas'] }); toast.success('Disciplina criada com sucesso') },
    onError: () => toast.error('Erro ao criar disciplina'),
  })
}

function useUpdateDisciplina() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ id, body }: { id: number; body: DisciplinaFormData }) =>
      api.put(`/admin/disciplinas/${id}`, body).then((r) => r.data),
    onSuccess: async () => { await qc.invalidateQueries({ queryKey: ['disciplinas'] }); toast.success('Disciplina atualizada') },
    onError: () => toast.error('Erro ao atualizar disciplina'),
  })
}

interface DisciplinaModalProps {
  open: boolean
  onClose: () => void
  initial?: DisciplinaOut | null
}

function DisciplinaModal({ open, onClose, initial }: DisciplinaModalProps) {
  const createMutation = useCreateDisciplina()
  const updateMutation = useUpdateDisciplina()
  const isEdit = !!initial

  const { register, handleSubmit, reset, formState: { errors } } = useForm<DisciplinaFormData>({
    resolver: zodResolver(disciplinaSchema),
    defaultValues: { nome: '', carga_horaria: null },
  })

  useEffect(() => {
    reset(initial ? { nome: initial.nome, carga_horaria: initial.carga_horaria ?? null } : { nome: '', carga_horaria: null })
  }, [initial, reset, open])

  const onSubmit = (data: DisciplinaFormData) => {
    if (isEdit && initial) {
      updateMutation.mutate({ id: initial.id, body: data }, { onSuccess: onClose })
    } else {
      createMutation.mutate(data, { onSuccess: onClose })
    }
  }

  const isPending = createMutation.isPending || updateMutation.isPending

  return (
    <Modal open={open} title={isEdit ? 'Editar Disciplina' : 'Nova Disciplina'} onClose={onClose}>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Nome *</label>
          <input {...register('nome')} className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="Ex: Matemática" />
          {errors.nome && <p className="mt-1 text-xs text-red-600">{errors.nome.message}</p>}
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Carga Horária (h/ano)</label>
          <input {...register('carga_horaria', { setValueAs: (v) => (v === '' ? null : Number(v)) })} type="number" min={1} className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="Ex: 120" />
        </div>
        <div className="flex justify-end gap-3 pt-2">
          <button type="button" onClick={onClose} className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50">Cancelar</button>
          <button type="submit" disabled={isPending} className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 disabled:opacity-50">{isPending ? 'Salvando...' : 'Salvar'}</button>
        </div>
      </form>
    </Modal>
  )
}

const COLUMNS = [
  { key: 'nome', label: 'Nome' },
  { key: 'carga_horaria', label: 'Carga Horária (h)' },
]

export default function DisciplinasPage() {
  const [page, setPage] = useState(1)
  const [search, setSearch] = useState('')
  const [modalOpen, setModalOpen] = useState(false)
  const [selected, setSelected] = useState<DisciplinaOut | null>(null)

  const { data, isLoading } = useDisciplinas(page, search)

  const openCreate = () => { setSelected(null); setModalOpen(true) }
  const openEdit = (row: Record<string, unknown>) => { setSelected(row as unknown as DisciplinaOut); setModalOpen(true) }

  return (
    <div className="p-8">
      <h1 className="text-2xl font-semibold text-gray-900 mb-6">Disciplinas</h1>
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
        onDeactivate={() => {}}
        isLoading={isLoading}
        onNew={openCreate}
        newLabel="Nova Disciplina"
      />
      <DisciplinaModal open={modalOpen} onClose={() => setModalOpen(false)} initial={selected} />
    </div>
  )
}
