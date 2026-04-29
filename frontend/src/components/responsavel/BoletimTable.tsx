import { StatusBadge } from './StatusBadge'

interface DisciplinaBoletimRow {
  disciplina_id: number
  disciplina_nome: string
  bim1: number | null
  bim2: number | null
  bim3: number | null
  bim4: number | null
  media: number | null
  total_aulas: number
  total_presentes: number
  freq_pct: number | null
  status: 'aprovado' | 'reprovado' | 'em_andamento'
}

interface BoletimTableProps {
  rows: DisciplinaBoletimRow[]
}

function formatNota(val: number | null): string {
  if (val === null) return '—'
  return val.toFixed(1)
}

function isAtRisk(row: DisciplinaBoletimRow): boolean {
  return (
    (row.freq_pct !== null && row.freq_pct < 75) ||
    (row.media !== null && row.media < 5.0)
  )
}

export function BoletimTable({ rows }: BoletimTableProps) {
  const thClass = 'px-3 py-2 text-xs font-semibold text-gray-500 uppercase tracking-wider'

  return (
    <div>
      <div className="overflow-x-auto">
        <table className="min-w-[640px] min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th scope="col" className={`${thClass} text-left`}>Disciplina</th>
              <th scope="col" className={`${thClass} text-center`}>1º Bim.</th>
              <th scope="col" className={`${thClass} text-center`}>2º Bim.</th>
              <th scope="col" className={`${thClass} text-center`}>3º Bim.</th>
              <th scope="col" className={`${thClass} text-center`}>4º Bim.</th>
              <th scope="col" className={`${thClass} text-center`}>Média</th>
              <th scope="col" className={`${thClass} text-center`}>Frequência</th>
              <th scope="col" className={`${thClass} text-center`}>Status</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {rows.map((row) => {
              const atRisk = isAtRisk(row)
              const rowClass = atRisk
                ? 'bg-red-50 hover:bg-red-100'
                : 'hover:bg-gray-50'
              const lowFreq = row.freq_pct !== null && row.freq_pct < 75
              const lowMedia = row.media !== null && row.media < 5.0
              const freqDisplay =
                row.freq_pct !== null
                  ? `${row.freq_pct.toFixed(0)}% (${row.total_presentes}/${row.total_aulas})`
                  : '—'

              return (
                <tr key={row.disciplina_id} className={rowClass}>
                  <td className="px-3 py-2 text-sm font-semibold text-gray-900 whitespace-nowrap">
                    {row.disciplina_nome}
                  </td>
                  {([row.bim1, row.bim2, row.bim3, row.bim4] as (number | null)[]).map((nota, i) => (
                    <td
                      key={i}
                      className={`px-3 py-2 text-sm text-center whitespace-nowrap ${
                        nota === null ? 'text-gray-400' : 'text-gray-700'
                      }`}
                    >
                      {formatNota(nota)}
                    </td>
                  ))}
                  <td
                    className={`px-3 py-2 text-sm text-center font-semibold whitespace-nowrap ${
                      lowMedia ? 'text-red-700' : 'text-gray-900'
                    }`}
                  >
                    {formatNota(row.media)}
                  </td>
                  <td
                    className={`px-3 py-2 text-sm text-center whitespace-nowrap ${
                      lowFreq ? 'text-red-700 font-semibold' : 'text-gray-700'
                    }`}
                  >
                    {freqDisplay}
                  </td>
                  <td className="px-3 py-2 text-center whitespace-nowrap">
                    <StatusBadge status={row.status} />
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
      <p className="text-xs text-gray-500 mt-4">
        Média calculada automaticamente. Aprovação exige média ≥ 5,0 e frequência ≥ 75% (LDB art. 24, VI).
      </p>
    </div>
  )
}
