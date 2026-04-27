interface AttendanceToggleProps {
  presente: boolean
  onChange: (presente: boolean) => void
}

export function AttendanceToggle({ presente, onChange }: AttendanceToggleProps) {
  return (
    <div className="flex rounded-md shadow-sm" role="group">
      <button
        type="button"
        aria-pressed={presente}
        onClick={() => onChange(true)}
        className={`px-3 py-1 text-xs font-medium rounded-l-md border ${
          presente
            ? 'bg-green-100 text-green-800 border-green-200'
            : 'bg-white text-gray-500 border-gray-300 hover:bg-gray-50'
        }`}
      >
        Presente
      </button>
      <button
        type="button"
        aria-pressed={!presente}
        onClick={() => onChange(false)}
        className={`px-3 py-1 text-xs font-medium rounded-r-md border -ml-px ${
          !presente
            ? 'bg-red-100 text-red-800 border-red-200'
            : 'bg-white text-gray-500 border-gray-300 hover:bg-gray-50'
        }`}
      >
        Falta
      </button>
    </div>
  )
}
