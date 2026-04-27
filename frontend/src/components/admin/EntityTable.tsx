interface Column {
  key: string
  label: string
}

interface EntityTableProps {
  columns: Column[]
  rows: Record<string, unknown>[]
  total: number
  page: number
  perPage: number
  search: string
  onPageChange: (page: number) => void
  onSearch: (q: string) => void
  onEdit: (row: Record<string, unknown>) => void
  onDeactivate: (row: Record<string, unknown>) => void
  isLoading?: boolean
  onNew?: () => void
  newLabel?: string
}

export function EntityTable({
  columns,
  rows,
  total,
  page,
  perPage,
  search,
  onPageChange,
  onSearch,
  onEdit,
  onDeactivate,
  isLoading,
  onNew,
  newLabel = 'Novo',
}: EntityTableProps) {
  const totalPages = Math.ceil(total / perPage)

  return (
    <div>
      <div className="flex items-center justify-between mb-4 gap-3">
        <input
          type="text"
          value={search}
          onChange={(e) => onSearch(e.target.value)}
          placeholder="Buscar por nome..."
          className="flex-1 max-w-xs px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />
        {onNew && (
          <button
            onClick={onNew}
            className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md hover:bg-indigo-700"
          >
            {newLabel}
          </button>
        )}
      </div>

      {isLoading ? (
        <div className="text-center py-12 text-gray-400 text-sm">Carregando...</div>
      ) : rows.length === 0 ? (
        <div className="text-center py-12 text-gray-400 text-sm">Nenhum registro encontrado.</div>
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                {columns.map((col) => (
                  <th
                    key={col.key}
                    className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    {col.label}
                  </th>
                ))}
                <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Ações
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {rows.map((row, i) => (
                <tr key={(row.id as number) ?? i} className="hover:bg-gray-50">
                  {columns.map((col) => (
                    <td key={col.key} className="px-4 py-3 text-sm text-gray-700 whitespace-nowrap">
                      {col.key === 'ativo' ? (
                        <span
                          className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${
                            row[col.key] ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                          }`}
                        >
                          {row[col.key] ? 'Ativo' : 'Inativo'}
                        </span>
                      ) : (
                        String(row[col.key] ?? '—')
                      )}
                    </td>
                  ))}
                  <td className="px-4 py-3 text-right whitespace-nowrap space-x-2">
                    <button
                      onClick={() => onEdit(row)}
                      className="text-xs font-medium text-indigo-600 hover:text-indigo-800"
                    >
                      Editar
                    </button>
                    {(row.ativo === true || row.ativo === undefined) && (
                      <button
                        onClick={() => onDeactivate(row)}
                        className="text-xs font-medium text-red-600 hover:text-red-800"
                      >
                        Desativar
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {totalPages > 1 && (
        <div className="flex items-center justify-between mt-4 text-sm text-gray-600">
          <span>
            {total} registro{total !== 1 ? 's' : ''}
          </span>
          <div className="flex gap-2">
            <button
              onClick={() => onPageChange(page - 1)}
              disabled={page <= 1}
              className="px-3 py-1 border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-40"
            >
              Anterior
            </button>
            <span className="px-3 py-1">
              {page} / {totalPages}
            </span>
            <button
              onClick={() => onPageChange(page + 1)}
              disabled={page >= totalPages}
              className="px-3 py-1 border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-40"
            >
              Próxima
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
