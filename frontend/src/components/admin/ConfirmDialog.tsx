import { Modal } from './Modal'

interface ConfirmDialogProps {
  open: boolean
  entityName: string
  onClose: () => void
  onConfirm: () => void
  loading?: boolean
}

export function ConfirmDialog({ open, entityName, onClose, onConfirm, loading }: ConfirmDialogProps) {
  return (
    <Modal open={open} title="Confirmar desativação" onClose={onClose}>
      <p className="text-sm text-gray-700 mb-6">
        Desativar <strong>{entityName}</strong>? Esta ação pode ser revertida.
      </p>
      <div className="flex justify-end gap-3">
        <button
          onClick={onClose}
          disabled={loading}
          className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50"
        >
          Cancelar
        </button>
        <button
          onClick={onConfirm}
          disabled={loading}
          className="px-4 py-2 text-sm font-medium text-white bg-red-600 border border-transparent rounded-md hover:bg-red-700 disabled:opacity-50"
        >
          {loading ? 'Desativando...' : 'Desativar'}
        </button>
      </div>
    </Modal>
  )
}
