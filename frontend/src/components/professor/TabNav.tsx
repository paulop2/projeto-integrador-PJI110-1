type Tab = 'chamada' | 'notas' | 'frequencia'

interface TabNavProps {
  active: Tab
  onChange: (tab: Tab) => void
}

export function TabNav({ active, onChange }: TabNavProps) {
  const tabs: { key: Tab; label: string }[] = [
    { key: 'chamada', label: 'Chamada' },
    { key: 'notas', label: 'Notas' },
    { key: 'frequencia', label: 'Frequencia' },
  ]
  return (
    <div className="border-b border-gray-200 mb-6" role="tablist">
      <div className="flex gap-6">
        {tabs.map((t) => (
          <button
            key={t.key}
            role="tab"
            aria-selected={active === t.key}
            onClick={() => onChange(t.key)}
            className={`px-1 py-3 text-sm font-medium border-b-2 ${
              active === t.key
                ? 'text-indigo-600 border-indigo-600'
                : 'text-gray-500 hover:text-gray-700 border-transparent'
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>
    </div>
  )
}
