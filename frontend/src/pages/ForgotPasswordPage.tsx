import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useMutation } from '@tanstack/react-query'
import { api } from '../services/api'

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState('')
  const [emailError, setEmailError] = useState('')
  const [submitted, setSubmitted] = useState(false)
  const [error, setError] = useState('')

  const mutation = useMutation({
    mutationFn: (body: { email: string }) =>
      api.post('/auth/forgot-password', body).then((r) => r.data),
    onSuccess: () => setSubmitted(true),
    onError: () => {
      setError('Não foi possível enviar o email. Tente novamente.')
    },
  })

  const validateEmail = () => {
    if (!email.trim()) {
      setEmailError('Email é obrigatório')
      return false
    }
    setEmailError('')
    return true
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    if (validateEmail()) {
      mutation.mutate({ email })
    }
  }

  if (submitted) {
    return (
      <div className="mx-auto mt-16 max-w-md px-6">
        <div className="rounded-lg border border-green-200 bg-green-50 p-6 text-center">
          <h2 className="mb-2 text-xl font-semibold text-green-800">
            Email enviado
          </h2>
          <p className="text-sm text-green-700">
            Email enviado para {email}. Verifique sua caixa de entrada e a pasta de spam.
          </p>
          <Link
            to="/login"
            className="mt-4 inline-block text-sm font-medium text-indigo-600 hover:underline"
          >
            Voltar para o login
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="mx-auto mt-16 max-w-md px-6">
      <h2 className="mb-2 text-2xl font-semibold text-gray-800">
        Recuperar Senha
      </h2>
      <p className="mb-6 text-sm text-gray-600">
        Insira seu email e enviaremos um link de recuperação
      </p>

      <form onSubmit={handleSubmit} noValidate>
        <div className="mb-4">
          <label htmlFor="email" className="mb-1 block text-sm font-medium text-gray-700">
            Email
          </label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => {
              setEmail(e.target.value)
              if (emailError) setEmailError('')
            }}
            onBlur={validateEmail}
            className={`w-full rounded-md border px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-indigo-500 ${
              emailError ? 'border-red-500' : 'border-gray-300'
            }`}
            placeholder="seu@email.com"
          />
          {emailError && (
            <p className="mt-1 text-xs text-red-600">{emailError}</p>
          )}
        </div>

        <button
          type="submit"
          disabled={mutation.isPending}
          className="w-full rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {mutation.isPending ? 'Enviando...' : 'Enviar link'}
        </button>

        {error && (
          <p className="mt-3 text-center text-sm text-red-600">{error}</p>
        )}
      </form>

      <div className="mt-4 text-center">
        <Link to="/login" className="text-sm text-indigo-600 hover:underline">
          Voltar para o login
        </Link>
      </div>
    </div>
  )
}
