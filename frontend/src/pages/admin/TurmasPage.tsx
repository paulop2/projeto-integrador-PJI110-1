import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient, keepPreviousData } from '@tanstack/react-query'
import { useForm, useFieldArray } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { toast } from 'sonner'
import { api } from '../../services/api'
import { EntityTable } from '../../components/admin/EntityTable'
import { Modal } from '../../components/admin/Modal'

interface TurmaOut {
  id: number
  nome: string
  ano: number
  serie: string
  turno: string
  professor_turma: { disciplina_id: number; professor_id: number }[]
}

interface ProfessorSelectItem {
  id: number
  nome: string
}

interface DisciplinaSelectItem {
  id: number
  nome: string
}

const professorTurmaRowSchema = z.object({
  disciplina_id: z.number().int().positive('Selecione uma disciplina'),
  professor_id: z.number().int().positive('Selecione um professor'),
})

const turmaSchema = z.object({
  nome: z.string().min(1, 'Nome é obrigatório'),
  ano: z.number().int().min(2000).max(2099),
  serie: z.string().min(1, 'Série é obrigatória'),
  turno: z.string().min(1, 'Turno é obrigatório'),
  professor_turma: z.array(professorTurmaRowSchema),
})
type TurmaFormData = z.infer<typeof turmaSchema>

function useTurmas(page: number, search: string) {
  return useQuery({
    queryKey: ['turmas', { page, search }],
    queryFn: () => api.get('/admin/turmas', { params: { page, search } }).then((r) => r.data),
    placeholderData: keepPreviousData,
  })
}

function useProfessoresSelect() {
  return useQuery<ProfessorSelectItem[]>({
    queryKey: ['professores-select'],
    queryFn: () => api.get('/admin/professores', { params: { page: 1, search: '' } }).then((r) => r.data.items),
  })
}

function useDisciplinasSelect() {
  return useQuery<DisciplinaSelectItem[]>({
    queryKey: ['disciplinas-select'],
    queryFn: () => api.get('/admin/disciplinas', { params: { page: 1, search: '' } }).then((r) => r.data.items),
  })
}

function useCreateTurma() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (body: TurmaFormData) => api.post('/admin/turmas', body).then((r) => r.data),
    onSuccess: async () => { await qc.invalidateQueries({ queryKey: ['turmas'] }); await qc.invalidateQueries({ queryKey: ['turmas-select'] }); toast.success('Turma criada com sucesso') },
  })
}

function useUpdateTurma() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ id, body }: { id: number; body: TurmaFormData }) =>
      api.put(`/admin/turmas/${id}`, body).then((r) => r.data),
    onSuccess: async () => { await qc.invalidateQueries({ queryKey: ['turmas'] }); await qc.invalidateQueries({ queryKey: ['turmas-select'] }); toast.success('Turma atualizada com sucesso') },
  })
}

interface TurmaModalProps {
  open: boolean
  onClose: () => void
  initial?: TurmaOut | null
}

function TurmaModal({ open, onClose, initial }: TurmaModalProps) {
  const { data: professores } = useProfessoresSelect()
  const { data: disciplinas } = useDisciplinasSelect()
  const createMutation = useCreateTurma()
  const updateMutation = useUpdateTurma()
  const isEdit = !!initial

  const defaultValues: TurmaFormData = { nome: '', ano: new Date().getFullYear(), serie: '', turno: 'manhã', professor_turma: [] }

  const { register, handleSubmit, reset, control, formState: { errors } } = useForm<TurmaFormData>({
    resolver: zodResolver(turmaSchema),
    defaultValues,
  })

  const { fields, append, remove } = useFieldArray({ control, name: 'professor_turma' })

  useEffect(() => {
    if (!open) return
    reset(
      initial
        ? { nome: initial.nome, ano: initial.ano, serie: initial.serie, turno: initial.turno, professor_turma: initial.professor_turma ?? [] }
        : defaultValues
    )
  }, [initial, reset])

  const onSubmit = (data: TurmaFormData) => {
    if (isEdit && initial) {
      updateMutation.mutate({ id: initial.id, body: data }, { onSuccess: onClose })
    } else {
      createMutation.mutate(data, { onSuccess: onClose })
    }
  }

  const isPending = createMutation.isPending || updateMutation.isPending

  return (
    <Modal open={open} title={isEdit ? 'Editar Turma' : 'Nova Turma'} onClose={onClose}>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Nome *</label>
            <input {...register('nome')} className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="Ex: 9A" />
            {errors.nome && <p className="mt-1 text-xs text-red-600">{errors.nome.message}</p>}
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Ano *</label>
            <input {...register('ano', { valueAsNumber: true })} type="number" className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Série *</label>
            <input {...register('serie')} className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="Ex: 9º ano" />
            {errors.serie && <p className="mt-1 text-xs text-red-600">{errors.serie.message}</p>}
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Turno *</label>
            <select {...register('turno')} className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
              <option value="manhã">Manhã</option>
              <option value="tarde">Tarde</option>
              <option value="noite">Noite</option>
            </select>
          </div>
        </div>

        <div>
          <div className="flex items-center justify-between mb-2">
            <label className="text-sm font-medium text-gray-700">Professores por Disciplina</label>
            <button
              type="button"
              onClick={() => append({ disciplina_id: 0, professor_id: 0 })}
              className="text-xs text-indigo-600 hover:text-indigo-800 font-medium"
            >
              + Adicionar linha
            </button>
          </div>
          {fields.length === 0 && (
            <p className="text-xs text-gray-400 py-2">Nenhum vínculo professor/disciplina. Clique em "Adicionar linha".</p>
          )}
          {fields.map((field, index) => (
            <div key={field.id} className="flex gap-2 mb-2 items-center">
              <select
                {...register(`professor_turma.${index}.disciplina_id`, { valueAsNumber: true })}
                className="flex-1 px-2 py-1.5 border border-gray-300 rounded text-sm"
              >
                <option value={0}>Disciplina...</option>
                {(disciplinas ?? []).map((d) => (
                  <option key={d.id} value={d.id}>{d.nome}</option>
                ))}
              </select>
              <select
                {...register(`professor_turma.${index}.professor_id`, { valueAsNumber: true })}
                className="flex-1 px-2 py-1.5 border border-gray-300 rounded text-sm"
              >
                <option value={0}>Professor...</option>
                {(professores ?? []).map((p) => (
                  <option key={p.id} value={p.id}>{p.nome}</option>
                ))}
              </select>
              <button type="button" onClick={() => remove(index)} className="text-red-500 hover:text-red-700 text-lg leading-none px-1">&times;</button>
            </div>
          ))}
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
  { key: 'serie', label: 'Série' },
  { key: 'turno', label: 'Turno' },
  { key: 'ano', label: 'Ano' },
]

export default function TurmasPage() {
  const [page, setPage] = useState(1)
  const [search, setSearch] = useState('')
  const [modalOpen, setModalOpen] = useState(false)
  const [selected, setSelected] = useState<TurmaOut | null>(null)

  const { data, isLoading } = useTurmas(page, search)

  const openCreate = () => { setSelected(null); setModalOpen(true) }
  const openEdit = (row: TurmaOut) => { setSelected(row); setModalOpen(true) }

  return (
    <div className="p-8">
      <h1 className="text-2xl font-semibold text-gray-900 mb-6">Turmas</h1>
      <EntityTable<TurmaOut>
        columns={COLUMNS}
        rows={(data?.items ?? []) as TurmaOut[]}
        total={data?.total ?? 0}
        page={page}
        perPage={25}
        search={search}
        onPageChange={setPage}
        onSearch={(q) => { setSearch(q); setPage(1) }}
        onEdit={openEdit}
        isLoading={isLoading}
        onNew={openCreate}
        newLabel="Nova Turma"
      />
      <TurmaModal open={modalOpen} onClose={() => setModalOpen(false)} initial={selected} />
    </div>
  )
}
