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

interface ResponsavelOut {
  id: number
  nome: string
  cpf: string | null
  telefone: string | null
  usuario_id: number
  email: string | null
}

interface AlunoSelectItem {
  id: number
  nome: string
  matricula: string | null
}

const createSchema = z.object({
  nome: z.string().min(1, 'Nome é obrigatório'),
  email: z.string().email('Email inválido'),
  senha: z.string().min(6, 'Senha deve ter pelo menos 6 caracteres'),
  cpf: z.string().nullable().optional(),
  telefone: z.string().nullable().optional(),
  aluno_ids: z.array(z.number()),
})
const updateSchema = z.object({
  nome: z.string().min(1, 'Nome é obrigatório'),
  cpf: z.string().nullable().optional(),
  telefone: z.string().nullable().optional(),
  aluno_ids: z.array(z.number()),
})
type ResponsavelCreateData = z.infer<typeof createSchema>
type ResponsavelUpdateData = z.infer<typeof updateSchema>

function useResponsaveis(page: number, search: string) {
  return useQuery({
    queryKey: ['responsaveis', { page, search }],
    queryFn: () => api.get('/admin/responsaveis', { params: { page, search } }).then((r) => r.data),
    placeholderData: keepPreviousData,
  })
}

function useAlunosForSelect() {
  return useQuery<AlunoSelectItem[]>({
    queryKey: ['alunos-select'],
    queryFn: () => api.get('/admin/alunos', { params: { page: 1, search: '' } }).then((r) => r.data.items),
  })
}

function useCreateResponsavel() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (body: ResponsavelCreateData) => api.post('/admin/responsaveis', body).then((r) => r.data),
    onSuccess: async () => { await qc.invalidateQueries({ queryKey: ['responsaveis'] }); await qc.invalidateQueries({ queryKey: ['alunos'] }); toast.success('Responsável criado com sucesso') },
    onError: (e: unknown) => {
      const msg = (e as { response?: { data?: { detail?: string } } })?.response?.data?.detail
      toast.error(msg ?? 'Erro ao criar responsável')
    },
  })
}

function useUpdateResponsavel() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ id, body }: { id: number; body: ResponsavelUpdateData }) =>
      api.put(`/admin/responsaveis/${id}`, body).then((r) => r.data),
    onSuccess: async () => { await qc.invalidateQueries({ queryKey: ['responsaveis'] }); await qc.invalidateQueries({ queryKey: ['alunos'] }); toast.success('Responsável atualizado') },
    onError: () => toast.error('Erro ao atualizar responsável'),
  })
}

function useDeactivateResponsavel() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (id: number) => api.post(`/admin/responsaveis/${id}/deactivate`).then((r) => r.data),
    onSuccess: async () => { await qc.invalidateQueries({ queryKey: ['responsaveis'] }); toast.success('Responsável desativado') },
    onError: () => toast.error('Erro ao desativar responsável'),
  })
}

interface ResponsavelModalProps {
  open: boolean
  onClose: () => void
  initial?: ResponsavelOut | null
}

function ResponsavelModal({ open, onClose, initial }: ResponsavelModalProps) {
  const { data: alunos } = useAlunosForSelect()
  const createMutation = useCreateResponsavel()
  const updateMutation = useUpdateResponsavel()
  const isEdit = !!initial

  const [selectedAlunoIds, setSelectedAlunoIds] = useState<number[]>([])

  const { register, handleSubmit, reset, setValue, formState: { errors } } = useForm<ResponsavelCreateData>({
    resolver: zodResolver(isEdit ? (updateSchema as unknown as typeof createSchema) : createSchema),
    defaultValues: { nome: '', email: '', senha: '', cpf: null, telefone: null, aluno_ids: [] },
  })

  useEffect(() => {
    const ids: number[] = []
    setSelectedAlunoIds(ids)
    reset(
      initial
        ? { nome: initial.nome, email: initial.email ?? '', senha: '', cpf: initial.cpf ?? null, telefone: initial.telefone ?? null, aluno_ids: ids }
        : { nome: '', email: '', senha: '', cpf: null, telefone: null, aluno_ids: [] }
    )
  }, [initial, reset, open])

  const toggleAluno = (id: number) => {
    const next = selectedAlunoIds.includes(id)
      ? selectedAlunoIds.filter((x) => x !== id)
      : [...selectedAlunoIds, id]
    setSelectedAlunoIds(next)
    setValue('aluno_ids', next)
  }

  const onSubmit = (data: ResponsavelCreateData) => {
    const payload = { ...data, aluno_ids: selectedAlunoIds }
    if (isEdit && initial) {
      updateMutation.mutate({ id: initial.id, body: { nome: payload.nome, cpf: payload.cpf, telefone: payload.telefone, aluno_ids: selectedAlunoIds } }, { onSuccess: onClose })
    } else {
      createMutation.mutate(payload, { onSuccess: onClose })
    }
  }

  const isPending = createMutation.isPending || updateMutation.isPending

  return (
    <Modal open={open} title={isEdit ? 'Editar Responsável' : 'Novo Responsável'} onClose={onClose}>
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
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">CPF</label>
            <input {...register('cpf')} className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="Opcional" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Telefone</label>
            <input {...register('telefone')} className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="Opcional" />
          </div>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Alunos vinculados</label>
          <div className="border border-gray-200 rounded-md max-h-36 overflow-y-auto divide-y divide-gray-100">
            {(alunos ?? []).length === 0 && (
              <p className="text-xs text-gray-400 p-3">Nenhum aluno cadastrado ainda.</p>
            )}
            {(alunos ?? []).map((aluno) => (
              <label key={aluno.id} className="flex items-center gap-2 px-3 py-2 hover:bg-gray-50 cursor-pointer">
                <input
                  type="checkbox"
                  checked={selectedAlunoIds.includes(aluno.id)}
                  onChange={() => toggleAluno(aluno.id)}
                  className="rounded border-gray-300 text-indigo-600"
                />
                <span className="text-sm text-gray-700">{aluno.nome}</span>
                {aluno.matricula && <span className="text-xs text-gray-400">({aluno.matricula})</span>}
              </label>
            ))}
          </div>
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
  { key: 'telefone', label: 'Telefone' },
]

export default function ResponsaveisPage() {
  const [page, setPage] = useState(1)
  const [search, setSearch] = useState('')
  const [modalOpen, setModalOpen] = useState(false)
  const [selected, setSelected] = useState<ResponsavelOut | null>(null)
  const [confirmOpen, setConfirmOpen] = useState(false)
  const [toDeactivate, setToDeactivate] = useState<ResponsavelOut | null>(null)

  const { data, isLoading } = useResponsaveis(page, search)
  const deactivateMutation = useDeactivateResponsavel()

  return (
    <div className="p-8">
      <h1 className="text-2xl font-semibold text-gray-900 mb-6">Responsáveis</h1>
      <EntityTable
        columns={COLUMNS}
        rows={(data?.items ?? []) as Record<string, unknown>[]}
        total={data?.total ?? 0}
        page={page}
        perPage={25}
        search={search}
        onPageChange={setPage}
        onSearch={(q) => { setSearch(q); setPage(1) }}
        onEdit={(row) => { setSelected(row as unknown as ResponsavelOut); setModalOpen(true) }}
        onDeactivate={(row) => { setToDeactivate(row as unknown as ResponsavelOut); setConfirmOpen(true) }}
        isLoading={isLoading}
        onNew={() => { setSelected(null); setModalOpen(true) }}
        newLabel="Novo Responsável"
      />
      <ResponsavelModal open={modalOpen} onClose={() => setModalOpen(false)} initial={selected} />
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
