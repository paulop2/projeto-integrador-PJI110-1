type EmptyStateVariant = 'no-children' | 'no-data'

interface EmptyStateProps {
  variant: EmptyStateVariant
}

export function EmptyState({ variant }: EmptyStateProps) {
  const config = {
    'no-children': {
      heading: 'Nenhum aluno vinculado',
      body: 'Entre em contato com a administração para vincular seu perfil a um aluno.',
    },
    'no-data': {
      heading: 'Boletim não disponível',
      body: 'As notas e frequências ainda não foram lançadas para este aluno.',
    },
  }[variant]

  return (
    <div className="text-center py-12">
      <svg
        className="mx-auto h-12 w-12 text-gray-300"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
        aria-hidden="true"
      >
        {variant === 'no-children' ? (
          // users icon
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={1.5}
            d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"
          />
        ) : (
          // file-text icon
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={1.5}
            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
          />
        )}
      </svg>
      <p className="text-xl font-semibold text-gray-900 mt-4">{config.heading}</p>
      <p className="text-sm text-gray-500 mt-2">{config.body}</p>
    </div>
  )
}
