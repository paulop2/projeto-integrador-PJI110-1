import { useState, useEffect } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { toast } from 'sonner'
import { api } from '../../services/api'

interface GradeTableProps {
  turmaId: number
  disciplinaId: number
}

export function GradeTable({ turmaId, disciplinaId }: GradeTableProps) {
  const qc = useQueryClient()
  const [grades, setGrades] = useState<Record<string, string>>({})

  const { data: notasData, isLoading } = useQuery({
    queryKey: ['notas', turmaId, disciplinaId],
    queryFn: () =>
      api.get(`/professor/turmas/${turmaId}/notas?disciplina_id=${disciplinaId}`).then((r) => r.data),
    enabled: disciplinaId > 0,
  })

  // Populate grades state when data loads
  useEffect(() => {
    if (!notasData) return
    const initial: Record<string, string> = {}
    for (const row of notasData) {
      for (const n of row.notas ?? []) {
        initial[`${row.aluno_id}-${n.bimestre}`] = String(n.valor)
      }
    }
    setGrades(initial)
  }, [notasData])

  const saveMutation = useMutation({
    mutationFn: (payload: { disciplina_id: number; grades: { aluno_id: number; bimestre: number; valor: number }[] }) =>
      api.post(`/professor/turmas/${turmaId}/notas`, payload).then((r) => r.data),
    onSuccess: async () => {
      await qc.invalidateQueries({ queryKey: ['notas', turmaId, disciplinaId] })
      toast.success('Notas salvas com sucesso.')
    },
    onError: () => toast.error('Erro ao salvar notas. Verifique os valores e tente novamente.'),
  })

  const handleChange = (alunoId: number, bimestre: number, value: string) => {
    setGrades((prev) => ({ ...prev, [`${alunoId}-${bimestre}`]: value }))
  }

  const isInvalid = (alunoId: number, bimestre: number): boolean => {
    const v = grades[`${alunoId}-${bimestre}`]
    if (v === '' || v === undefined) return false
    const num = parseFloat(v)
    return isNaN(num) || num < 0 || num > 10
  }

  const hasErrors = notasData?.some((_: unknown, idx: number) =>
    [1, 2, 3, 4].some((b) => isInvalid(notasData[idx].aluno_id, b))
  ) ?? false

  const handleSave = () => {
    if (!notasData) return
    const gradeList: { aluno_id: number; bimestre: number; valor: number }[] = []
    for (const row of notasData) {
      for (const b of [1, 2, 3, 4]) {
        const v = grades[`${row.aluno_id}-${b}`]
        if (v !== '' && v !== undefined) {
          gradeList.push({ aluno_id: row.aluno_id, bimestre: b, valor: parseFloat(v) })
        }
      }
    }
    saveMutation.mutate({ disciplina_id: disciplinaId, grades: gradeList })
  }

  if (isLoading) {
    return <div className="text-center py-12 text-gray-400 text-sm">Carregando notas...</div>
  }

  if (!notasData || notasData.length === 0) {
    return (
      <div className="text-center py-12 text-gray-400 text-sm">Nenhum aluno matriculado nesta turma.</div>
    )
  }

  return (
    <div>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Aluno
              </th>
              {[1, 2, 3, 4].map((b) => (
                <th
                  key={b}
                  className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  {b}o Bimestre
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {notasData.map((row: { aluno_id: number; nome: string; notas: unknown[] }) => (
              <tr key={row.aluno_id} className="hover:bg-gray-50">
                <td className="px-4 py-3 text-sm font-medium text-gray-900 whitespace-nowrap">
                  {row.nome}
                </td>
                {[1, 2, 3, 4].map((b) => (
                  <td key={b} className="px-2 py-2">
                    <input
                      type="text"
                      value={grades[`${row.aluno_id}-${b}`] ?? ''}
                      onChange={(e) => handleChange(row.aluno_id, b, e.target.value)}
                      placeholder="—"
                      aria-invalid={isInvalid(row.aluno_id, b)}
                      className={`w-20 px-2 py-1 border rounded-md text-sm text-center focus:outline-none focus:ring-2 ${
                        isInvalid(row.aluno_id, b)
                          ? 'border-red-500 focus:ring-red-500 bg-red-50'
                          : 'border-gray-300 focus:ring-indigo-500'
                      }`}
                    />
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="mt-4 flex justify-end">
        <button
          onClick={handleSave}
          disabled={saveMutation.isPending || hasErrors}
          className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md hover:bg-indigo-700 disabled:opacity-50"
        >
          {saveMutation.isPending ? 'Salvando...' : 'Salvar notas'}
        </button>
      </div>
    </div>
  )
}
