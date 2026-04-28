interface SkeletonCardProps {
  rows?: number
  className?: string
}

export function SkeletonCard({ rows = 3, className = '' }: SkeletonCardProps) {
  return (
    <div
      className={`bg-white rounded-lg border border-gray-200 p-4 space-y-3 ${className}`}
      aria-busy="true"
      role="status"
    >
      {/* Title block */}
      <div className="animate-pulse bg-gray-200 rounded h-5 w-[60%]" />
      {/* Content blocks */}
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="animate-pulse bg-gray-200 rounded h-4 w-full" />
      ))}
    </div>
  )
}
