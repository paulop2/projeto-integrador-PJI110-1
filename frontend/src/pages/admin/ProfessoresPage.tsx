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

interface ProfessorOut {
  id: number
  nome: string
  cpf: string | null
  usuario_id: number
  email: string | null
}

const createSchema = z.object({
  nome: z.string().min(1, 'Nome é obrigatório'),
  email: z.string().email('Email inválido'),
  senha: z.string().min(6, 'Senha deve ter pelo menos 6 caracteres'),
  cpf: z.string().nullable().optional(),
})
const updateSchema = z.object({
  nome: z.string().min(1, 'Nome é obrigatório'),
  cpf: z.string().nullable().optional(),
})
type ProfessorCreateData = z.infer<typeof createSchema>
type ProfessorUpdateData = z.infer<typeof updateSchema>

function useProfessores(page: number, search: string) {
  return useQuery({
    queryKey: ['professores', { page, search }],
    queryFn: () => api.get('/admin/professores', { params: { page, search } }).then((r) => r.data),
    placeholderData: keepPreviousData,
  })
}

function useCreateProfessor() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (body: ProfessorCreateData) => api.post('/admin/professores', body).then((r) => r.data),
    onSuccess: async () => { await qc.invalidateQueries({ queryKey: ['professores'] }); await qc.invalidateQueries({ queryKey: ['professores-select'] }); toast.success('Professor criado com sucesso') },
    onError: (e: unknown) => {
      const msg = (e as { response?: { data?: { detail?: string } } })?.response?.data?.detail
      toast.error(msg ?? 'Erro ao criar professor')
    },
  })
}

function useUpdateProfessor() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ id, body }: { id: number; body: ProfessorUpdateData }) =>
      api.put(`/admin/professores/${id}`, body).then((r) => r.data),
    onSuccess: async () => { await qc.invalidateQueries({ queryKey: ['professores'] }); await qc.invalidateQueries({ queryKey: ['professores-select'] }); toast.success('Professor atualizado') },
    onError: () => toast.error('Erro ao atualizar professor'),
  })
}

function useDeactivateProfessor() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (id: number) => api.post(`/admin/professores/${id}/deactivate`).then((r) => r.data),
    onSuccess: async () => { await qc.invalidateQueries({ queryKey: ['professores'] }); toast.success('Professor desativado') },
    onError: () => toast.error('Erro ao desativar professor'),
  })
}

interface ProfessorModalProps {
  open: boolean
  onClose: () => void
  initial?: ProfessorOut | null
}

function ProfessorModal({ open, onClose, initial }: ProfessorModalProps) {
  const createMutation = useCreateProfessor()
  const updateMutation = useUpdateProfessor()
  const isEdit = !!initial

  const { register, handleSubmit, reset, formState: { errors } } = useForm<ProfessorCreateData>({
    resolver: zodResolver(isEdit ? (updateSchema as unknown as typeof createSchema) : createSchema),
    defaultValues: { nome: '', email: '', senha: '', cpf: null },
  })

  useEffect(() => {
    reset(
      initial ? { nome: initial.nome, email: initial.email ?? '', senha: '', cpf: initial.cpf ?? null }
               : { nome: '', email: '', senha: '', cpf: null }
    )
  }, [initial, reset, open])

  const onSubmit = (data: ProfessorCreateData) => {
    if (isEdit && initial) {
      updateMutation.mutate({ id: initial.id, body: { nome: data.nome, cpf: data.cpf } }, { onSuccess: onClose })
    } else {
      createMutation.mutate(data, { onSuccess: onClose })
    }
  }

  const isPending = createMutation.isPending || updateMutation.isPending

  return (
    <Modal open={open} title={isEdit ? 'Editar Professor' : 'Novo Professor'} onClose={onClose}>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Nome *</label>
          <input {...register('nome')} className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
          {errors.nome && <p className="mt-1 text-xs text-red-600">{errors.nome.message}</p>}
        </div>
        {!isEdit && (
          <>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Email *</label>
              <input {...register('email')} type="email" className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
              {errors.email && <p className="mt-1 text-xs text-red-600">{errors.email.message}</p>}
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Senha inicial *</label>
              <input {...register('senha')} type="password" className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
              {errors.senha && <p className="mt-1 text-xs text-red-600">{errors.senha.message}</p>}
            </div>
          </>
        )}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">CPF</label>
          <input {...register('cpf')} className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="Opcional" />
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
  { key: 'email', label: 'Email' },
  { key: 'cpf', label: 'CPF' },
]

export default function ProfessoresPage() {
  const [page, setPage] = useState(1)
  const [search, setSearch] = useState('')
  const [modalOpen, setModalOpen] = useState(false)
  const [selected, setSelected] = useState<ProfessorOut | null>(null)
  const [confirmOpen, setConfirmOpen] = useState(false)
  const [toDeactivate, setToDeactivate] = useState<ProfessorOut | null>(null)

  const { data, isLoading } = useProfessores(page, search)
  const deactivateMutation = useDeactivateProfessor()

  return (
    <div className="p-8">
      <h1 className="text-2xl font-semibold text-gray-900 mb-6">Professores</h1>
      <EntityTable
        columns={COLUMNS}
        rows={(data?.items ?? []) as Record<string, unknown>[]}
        total={data?.total ?? 0}
        page={page}
        perPage={25}
        search={search}
        onPageChange={setPage}
        onSearch={(q) => { setSearch(q); setPage(1) }}
        onEdit={(row) => { setSelected(row as unknown as ProfessorOut); setModalOpen(true) }}
        onDeactivate={(row) => { setToDeactivate(row as unknown as ProfessorOut); setConfirmOpen(true) }}
        isLoading={isLoading}
        onNew={() => { setSelected(null); setModalOpen(true) }}
        newLabel="Novo Professor"
      />
      <ProfessorModal open={modalOpen} onClose={() => setModalOpen(false)} initial={selected} />
      <ConfirmDialog
        open={confirmOpen}
        entityName={toDeactivate?.nome ?? ''}
        onClose={() => setConfirmOpen(false)}
        onConfirm={() => toDeactivate && deactivateMutation.mutate(toDeactivate.id, { onSuccess: () => setConfirmOpen(false) })}
        loading={deactivateMutation.isPending}
      />
    </div>
  )
}
