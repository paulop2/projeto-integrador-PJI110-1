import { SkeletonTable } from '../SkeletonTable'

interface Column {
  key: string
  label: string
}

interface EntityTableProps<T> {
  columns: Column[]
  rows: T[]
  total: number
  page: number
  perPage: number
  search: string
  onPageChange: (page: number) => void
  onSearch: (q: string) => void
  onEdit: (row: T) => void
  onDeactivate?: (row: T) => void
  isLoading?: boolean
  onNew?: () => void
  newLabel?: string
}

export function EntityTable<T>({
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
}: EntityTableProps<T>) {
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
        <div className="overflow-x-auto">
          <SkeletonTable rows={5} columns={columns.length + 1} />
        </div>
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
              {rows.map((row, i) => {
                const r = row as Record<string, unknown> & { id?: number; ativo?: boolean }
                return (
                  <tr key={r.id ?? i} className="hover:bg-gray-50">
                    {columns.map((col) => (
                      <td key={col.key} className="px-4 py-3 text-sm text-gray-700 whitespace-nowrap">
                        {col.key === 'ativo' ? (
                          <span
                            className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${
                              r.ativo ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                            }`}
                          >
                            {r.ativo ? 'Ativo' : 'Inativo'}
                          </span>
                        ) : (
                          String(r[col.key] ?? '—')
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
                      {onDeactivate && (r.ativo === true || r.ativo === undefined) && (
                        <button
                          onClick={() => onDeactivate(row)}
                          className="text-xs font-medium text-red-600 hover:text-red-800"
                        >
                          Desativar
                        </button>
                      )}
                    </td>
                  </tr>
                )
              })}
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
