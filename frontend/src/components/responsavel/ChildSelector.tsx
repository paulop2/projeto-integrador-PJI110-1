interface FilhoOut {
  id: number
  nome: string
  turma_nome: string | null
}

interface ChildSelectorProps {
  filhos: FilhoOut[]
  selectedId: number | null
  onChange: (id: number) => void
}

export function ChildSelector({ filhos, selectedId, onChange }: ChildSelectorProps) {
  // Only show selector when responsavel has multiple children (UI-SPEC 1.1)
  if (filhos.length <= 1) return null

  return (
    <div className="mb-6">
      <label className="block text-sm font-normal text-gray-700 mb-1">
        Filho(a)
      </label>
      <select
        value={selectedId ?? ''}
        onChange={(e) => onChange(Number(e.target.value))}
        className="w-full sm:w-72 border border-gray-300 rounded-md text-sm px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white"
      >
        {filhos.map((f) => (
          <option key={f.id} value={f.id}>
            {f.nome}{f.turma_nome ? ` — ${f.turma_nome}` : ''}
          </option>
        ))}
      </select>
    </div>
  )
}
