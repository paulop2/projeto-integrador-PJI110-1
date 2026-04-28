interface SkeletonRowProps {
  columns?: number
  className?: string
}

export function SkeletonRow({ columns = 4, className = '' }: SkeletonRowProps) {
  return (
    <div className={`flex gap-4 animate-pulse ${className}`}>
      {Array.from({ length: columns }).map((_, i) => (
        <div
          key={i}
          className="bg-gray-200 rounded h-4 flex-1"
          style={{ maxWidth: `${70 + (i % 3) * 15}%` }}
        />
      ))}
    </div>
  )
}
