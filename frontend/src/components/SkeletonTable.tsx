import { SkeletonRow } from './SkeletonRow'

interface SkeletonTableProps {
  rows?: number
  columns?: number
}

export function SkeletonTable({ rows = 5, columns = 4 }: SkeletonTableProps) {
  return (
    <div className="border border-gray-200 rounded-lg overflow-hidden divide-y divide-gray-100">
      {/* Header row */}
      <div className="p-4 bg-gray-50">
        <SkeletonRow columns={columns} className="opacity-80" />
      </div>
      {/* Data rows */}
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="p-4">
          <SkeletonRow columns={columns} />
        </div>
      ))}
    </div>
  )
}
