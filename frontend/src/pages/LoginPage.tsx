import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
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

export default function LoginPage() {
  const navigate = useNavigate()
  const { login } = useAuth()

  const [email, setEmail] = useState('')
  const [senha, setSenha] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [emailError, setEmailError] = useState('')
  const [senhaError, setSenhaError] = useState('')
  const [loginError, setLoginError] = useState('')

  const mutation = useMutation({
    mutationFn: (body: { email: string; senha: string }) =>
      api.post('/auth/login', body).then((r) => r.data),
    onSuccess: (data: { access_token: string; user: { id: number; email: string; tipo: 'admin' | 'professor' | 'responsavel'; nome: string } }) => {
      login(data.access_token, data.user)
      navigate(`/${data.user.tipo}`, { replace: true })
    },
    onError: () => {
      setLoginError('Email ou senha incorretos')
    },
  })

  const validateEmail = () => {
    if (!email.trim()) {
      setEmailError('Email é obrigatório')
      return false
    }
    if (!email.includes('@')) {
      setEmailError('Email inválido')
      return false
    }
    setEmailError('')
    return true
  }

  const validateSenha = () => {
    if (!senha.trim()) {
      setSenhaError('Senha é obrigatória')
      return false
    }
    setSenhaError('')
    return true
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setLoginError('')
    const isEmailValid = validateEmail()
    const isSenhaValid = validateSenha()
    if (isEmailValid && isSenhaValid) {
      mutation.mutate({ email, senha })
    }
  }

  return (
    <div className="flex h-screen w-full">
      {/* Left side */}
      <div className="hidden w-2/5 flex-col items-center justify-center bg-indigo-700 text-white md:flex">
        <h1 className="text-4xl font-bold">Sistema Escolar</h1>
        <p className="mt-4 text-center text-lg opacity-90">
          Acompanhe o desempenho escolar dos seus filhos
        </p>
      </div>

      {/* Right side */}
      <div className="flex w-full flex-col items-center justify-center bg-white md:w-3/5">
        <div className="w-full max-w-md px-6">
          <h2 className="mb-6 text-2xl font-semibold text-gray-800">
            Acesso ao Sistema
          </h2>

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

            <div className="mb-2">
              <label htmlFor="senha" className="mb-1 block text-sm font-medium text-gray-700">
                Senha
              </label>
              <div className="relative">
                <input
                  id="senha"
                  type={showPassword ? 'text' : 'password'}
                  value={senha}
                  onChange={(e) => {
                    setSenha(e.target.value)
                    if (senhaError) setSenhaError('')
                  }}
                  onBlur={validateSenha}
                  className={`w-full rounded-md border px-3 py-2 pr-10 text-sm outline-none focus:ring-2 focus:ring-indigo-500 ${
                    senhaError ? 'border-red-500' : 'border-gray-300'
                  }`}
                  placeholder="Sua senha"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword((prev) => !prev)}
                  className="absolute right-2 top-1/2 -translate-y-1/2 p-1"
                  tabIndex={-1}
                  aria-label={showPassword ? 'Ocultar senha' : 'Mostrar senha'}
                >
                  <EyeIcon open={showPassword} />
                </button>
              </div>
              {senhaError && (
                <p className="mt-1 text-xs text-red-600">{senhaError}</p>
              )}
            </div>

            <div className="mb-6 text-right">
              <Link
                to="/esqueci-senha"
                className="text-sm text-indigo-600 hover:underline"
              >
                Esqueci minha senha
              </Link>
            </div>

            <button
              type="submit"
              disabled={mutation.isPending}
              className="w-full rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {mutation.isPending ? 'Carregando...' : 'Entrar'}
            </button>

            {loginError && (
              <p className="mt-3 text-center text-sm text-red-600">{loginError}</p>
            )}
          </form>
        </div>
      </div>
    </div>
  )
}
