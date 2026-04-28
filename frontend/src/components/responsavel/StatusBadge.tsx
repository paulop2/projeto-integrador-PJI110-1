interface StatusBadgeProps {
  aprovado: boolean
}

export function StatusBadge({ aprovado }: StatusBadgeProps) {
  return (
    <span
      className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold ${
        aprovado
          ? 'bg-green-100 text-green-800'
          : 'bg-red-100 text-red-800'
      }`}
    >
      {aprovado ? 'Aprovado' : 'Reprovado'}
    </span>
  )
}
