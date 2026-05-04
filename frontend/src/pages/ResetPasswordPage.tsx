import { useState } from 'react'
import { Link, useNavigate, useSearchParams } from 'react-router-dom'
import { useMutation } from '@tanstack/react-query'
import { useAuth } from '../contexts/AuthContext'
import { api } from '../services/api'

function EyeIcon({ open }: { open: boolean }) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="20"
      height="20"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      className="text-gray-500"
    >
      {open ? (
        <>
          <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7z" />
          <circle cx="12" cy="12" r="3" />
        </>
      ) : (
        <>
          <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24" />
          <line x1="1" y1="1" x2="23" y2="23" />
        </>
      )}
    </svg>
  )
}

export default function ResetPasswordPage() {
  const navigate = useNavigate()
  const { login } = useAuth()
  const [params] = useSearchParams()
  const token = params.get('token')

  const [novaSenha, setNovaSenha] = useState('')
  const [confirmarSenha, setConfirmarSenha] = useState('')
  const [showNovaSenha, setShowNovaSenha] = useState(false)
  const [showConfirmarSenha, setShowConfirmarSenha] = useState(false)
  const [capsLockOn, setCapsLockOn] = useState(false)
  const [novaSenhaError, setNovaSenhaError] = useState('')
  const [confirmarSenhaError, setConfirmarSenhaError] = useState('')
  const [error, setError] = useState('')

  const mutation = useMutation({
    mutationFn: (body: { token: string; nova_senha: string }) =>
      api.post('/auth/reset-password', body).then((r) => r.data),
    onSuccess: (data: { access_token: string; user: { id: number; email: string; tipo: 'admin' | 'professor' | 'responsavel'; nome: string } }) => {
      login(data.access_token, data.user)
      navigate(`/${data.user.tipo}`, { replace: true })
    },
    onError: () => {
      setError('Link de recuperação inválido ou expirado.')
    },
  })

  const validateNovaSenha = () => {
    if (!novaSenha.trim()) {
      setNovaSenhaError('Nova senha é obrigatória')
      return false
    }
    if (novaSenha.length < 8) {
      setNovaSenhaError('A senha deve ter no mínimo 8 caracteres')
      return false
    }
    setNovaSenhaError('')
    return true
  }

  const validateConfirmarSenha = () => {
    if (!confirmarSenha.trim()) {
      setConfirmarSenhaError('Confirmação de senha é obrigatória')
      return false
    }
    if (confirmarSenha !== novaSenha) {
      setConfirmarSenhaError('As senhas não coincidem')
      return false
    }
    setConfirmarSenhaError('')
    return true
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    const isNovaSenhaValid = validateNovaSenha()
    const isConfirmarValid = validateConfirmarSenha()
    if (isNovaSenhaValid && isConfirmarValid && token) {
      mutation.mutate({ token, nova_senha: novaSenha })
    }
  }

  const handlePasswordKeyState = (e: React.KeyboardEvent<HTMLInputElement>) => {
    setCapsLockOn(e.getModifierState('CapsLock'))
  }

  if (!token) {
    return (
      <div className="mx-auto mt-16 max-w-md px-6">
        <div className="rounded-lg border border-red-200 bg-red-50 p-6 text-center">
          <h2 className="mb-2 text-xl font-semibold text-red-800">
            Link de recuperação inválido
          </h2>
          <p className="mb-4 text-sm text-red-700">
            O link que você acessou não é válido ou está incompleto.
          </p>
          <Link
            to="/esqueci-senha"
            className="text-sm font-medium text-indigo-600 hover:underline"
          >
            Solicitar novo link
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="mx-auto mt-16 max-w-md px-6">
      <h2 className="mb-6 text-2xl font-semibold text-gray-800">
        Nova Senha
      </h2>

      <form onSubmit={handleSubmit} noValidate>
        <div className="mb-4">
          <label htmlFor="nova-senha" className="mb-1 block text-sm font-medium text-gray-700">
            Nova senha
          </label>
          <div className="relative">
            <input
              id="nova-senha"
              type={showNovaSenha ? 'text' : 'password'}
              value={novaSenha}
              onChange={(e) => {
                setNovaSenha(e.target.value)
                if (novaSenhaError) setNovaSenhaError('')
              }}
              onBlur={validateNovaSenha}
              onKeyUp={handlePasswordKeyState}
              onClick={handlePasswordKeyState}
              className={`w-full rounded-md border px-3 py-2 pr-10 text-sm outline-none focus:ring-2 focus:ring-indigo-500 ${
                novaSenhaError ? 'border-red-500' : 'border-gray-300'
              }`}
              placeholder="Mínimo 8 caracteres"
              autoComplete="new-password"
              aria-invalid={Boolean(novaSenhaError)}
              aria-describedby={novaSenhaError || capsLockOn ? 'nova-senha-help' : undefined}
            />
            <button
              type="button"
              onClick={() => setShowNovaSenha((prev) => !prev)}
              className="absolute right-2 top-1/2 -translate-y-1/2 p-1"
              aria-label={showNovaSenha ? 'Ocultar senha' : 'Mostrar senha'}
            >
              <EyeIcon open={showNovaSenha} />
            </button>
          </div>
          {(novaSenhaError || capsLockOn) && (
            <p id="nova-senha-help" className={`mt-1 text-xs ${novaSenhaError ? 'text-red-600' : 'text-amber-600'}`}>
              {novaSenhaError || 'Caps Lock ativado'}
            </p>
          )}
        </div>

        <div className="mb-6">
          <label htmlFor="confirmar-senha" className="mb-1 block text-sm font-medium text-gray-700">
            Confirmar senha
          </label>
          <div className="relative">
            <input
              id="confirmar-senha"
              type={showConfirmarSenha ? 'text' : 'password'}
              value={confirmarSenha}
              onChange={(e) => {
                setConfirmarSenha(e.target.value)
                if (confirmarSenhaError) setConfirmarSenhaError('')
              }}
              onBlur={validateConfirmarSenha}
              onKeyUp={handlePasswordKeyState}
              onClick={handlePasswordKeyState}
              className={`w-full rounded-md border px-3 py-2 pr-10 text-sm outline-none focus:ring-2 focus:ring-indigo-500 ${
                confirmarSenhaError ? 'border-red-500' : 'border-gray-300'
              }`}
              placeholder="Repita a nova senha"
              autoComplete="new-password"
              aria-invalid={Boolean(confirmarSenhaError)}
              aria-describedby={confirmarSenhaError || capsLockOn ? 'confirmar-senha-help' : undefined}
            />
            <button
              type="button"
              onClick={() => setShowConfirmarSenha((prev) => !prev)}
              className="absolute right-2 top-1/2 -translate-y-1/2 p-1"
              aria-label={showConfirmarSenha ? 'Ocultar senha' : 'Mostrar senha'}
            >
              <EyeIcon open={showConfirmarSenha} />
            </button>
          </div>
          {(confirmarSenhaError || capsLockOn) && (
            <p id="confirmar-senha-help" className={`mt-1 text-xs ${confirmarSenhaError ? 'text-red-600' : 'text-amber-600'}`}>
              {confirmarSenhaError || 'Caps Lock ativado'}
            </p>
          )}
        </div>

        <button
          type="submit"
          disabled={mutation.isPending}
          className="w-full rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {mutation.isPending ? 'Redefinindo...' : 'Redefinir senha'}
        </button>

        {error && (
          <div className="mt-4 text-center">
            <p role="alert" className="text-sm text-red-600">{error}</p>
            <Link
              to="/esqueci-senha"
              className="mt-2 inline-block text-sm text-indigo-600 hover:underline"
            >
              Solicitar novo link
            </Link>
          </div>
        )}
      </form>
    </div>
  )
}
