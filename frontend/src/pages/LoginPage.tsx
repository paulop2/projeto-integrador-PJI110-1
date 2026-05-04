import { useEffect, useRef, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useMutation } from '@tanstack/react-query'
import { useAuth } from '../contexts/AuthContext'
import { api } from '../services/api'

function EyeIcon({ open }: { open: boolean }) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="18"
      height="18"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      className="text-gray-400"
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
  const emailInputRef = useRef<HTMLInputElement>(null)

  const [email, setEmail] = useState('')
  const [senha, setSenha] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [capsLockOn, setCapsLockOn] = useState(false)
  const [emailError, setEmailError] = useState('')
  const [senhaError, setSenhaError] = useState('')
  const [loginError, setLoginError] = useState('')

  useEffect(() => {
    emailInputRef.current?.focus()
  }, [])

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
    if (!email.trim()) { setEmailError('Email é obrigatório'); return false }
    if (!email.includes('@')) { setEmailError('Email inválido'); return false }
    setEmailError('')
    return true
  }

  const validateSenha = () => {
    if (!senha.trim()) { setSenhaError('Senha é obrigatória'); return false }
    setSenhaError('')
    return true
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setLoginError('')
    const emailOk = validateEmail()
    const senhaOk = validateSenha()
    const ok = emailOk && senhaOk
    if (ok) mutation.mutate({ email, senha })
  }

  const handlePasswordKeyState = (e: React.KeyboardEvent<HTMLInputElement>) => {
    setCapsLockOn(e.getModifierState('CapsLock'))
  }

  return (
    <div className="flex h-screen w-full bg-white">
      {/* ── Left panel ── */}
      <div className="hidden md:flex w-2/5 flex-col relative overflow-hidden bg-indigo-700">
        {/* Subtle grid pattern */}
        <div
          className="absolute inset-0 opacity-10"
          style={{
            backgroundImage: 'linear-gradient(white 1px,transparent 1px),linear-gradient(90deg,white 1px,transparent 1px)',
            backgroundSize: '40px 40px',
          }}
        />
        {/* Gradient overlay bottom */}
        <div className="absolute bottom-0 left-0 right-0 h-48 bg-gradient-to-t from-indigo-900/60 to-transparent" />

        <div className="relative flex flex-col justify-center h-full px-12">
          {/* Logo mark */}
          <div className="w-14 h-14 rounded-2xl bg-white/15 backdrop-blur-sm flex items-center justify-center mb-8 ring-1 ring-white/20">
            <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M22 10v6M2 10l10-5 10 5-10 5z" />
              <path d="M6 12v5c3 3 9 3 12 0v-5" />
            </svg>
          </div>

          <h1 className="text-3xl font-bold text-white leading-tight mb-3">
            EscolaApp
          </h1>
          <p className="text-indigo-200 text-base leading-relaxed max-w-xs">
            Portal unificado para administração, professores e responsáveis.
          </p>

          {/* Feature list */}
          <ul className="mt-10 space-y-3">
            {[
              'Acompanhe notas e frequência em tempo real',
              'Gerencie turmas, disciplinas e alunos',
              'Comunicação direta com responsáveis',
            ].map((item) => (
              <li key={item} className="flex items-start gap-2.5 text-sm text-indigo-100">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" className="mt-0.5 flex-shrink-0 text-indigo-300">
                  <polyline points="20 6 9 17 4 12" />
                </svg>
                {item}
              </li>
            ))}
          </ul>
        </div>

        {/* Bottom tag */}
        <div className="relative px-12 pb-8">
          <p className="text-xs text-indigo-300/70">
            Projeto Integrador &middot; PJI110
          </p>
        </div>
      </div>

      {/* ── Right panel ── */}
      <div className="flex flex-1 flex-col items-center justify-center px-8">
        <div className="w-full max-w-sm">
          {/* Mobile logo */}
          <div className="flex items-center gap-2 mb-8 md:hidden">
            <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M22 10v6M2 10l10-5 10 5-10 5z" />
                <path d="M6 12v5c3 3 9 3 12 0v-5" />
              </svg>
            </div>
            <span className="text-lg font-bold text-gray-900">EscolaApp</span>
          </div>

          <h2 className="text-xl font-bold text-gray-900 mb-1">Entrar na conta</h2>
          <p className="text-sm text-gray-500 mb-8">Use suas credenciais para acessar o sistema.</p>

          <form onSubmit={handleSubmit} noValidate className="space-y-5">
            {/* Email */}
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1.5">
                Email
              </label>
              <input
                ref={emailInputRef}
                id="email"
                type="email"
                value={email}
                onChange={(e) => { setEmail(e.target.value); if (emailError) setEmailError('') }}
                onBlur={validateEmail}
                className={`w-full rounded-lg border px-3.5 py-2.5 text-sm text-gray-900 placeholder-gray-400 outline-none transition focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 ${
                  emailError ? 'border-red-400 bg-red-50' : 'border-gray-300 bg-white'
                }`}
                placeholder="seu@email.com"
                autoComplete="email"
                aria-invalid={Boolean(emailError)}
                aria-describedby={emailError ? 'email-error' : undefined}
              />
              {emailError && <p id="email-error" className="mt-1.5 text-xs text-red-600">{emailError}</p>}
            </div>

            {/* Senha */}
            <div>
              <div className="flex items-center justify-between mb-1.5">
                <label htmlFor="senha" className="block text-sm font-medium text-gray-700">
                  Senha
                </label>
                <Link to="/esqueci-senha" className="text-xs text-indigo-600 hover:text-indigo-700 hover:underline">
                  Esqueci minha senha
                </Link>
              </div>
              <div className="relative">
                <input
                  id="senha"
                  type={showPassword ? 'text' : 'password'}
                  value={senha}
                  onChange={(e) => { setSenha(e.target.value); if (senhaError) setSenhaError('') }}
                  onBlur={validateSenha}
                  onKeyUp={handlePasswordKeyState}
                  onClick={handlePasswordKeyState}
                  className={`w-full rounded-lg border px-3.5 py-2.5 pr-11 text-sm text-gray-900 placeholder-gray-400 outline-none transition focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 ${
                    senhaError ? 'border-red-400 bg-red-50' : 'border-gray-300 bg-white'
                  }`}
                  placeholder="Sua senha"
                  autoComplete="current-password"
                  aria-invalid={Boolean(senhaError)}
                  aria-describedby={senhaError || capsLockOn ? 'senha-help' : undefined}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword((v) => !v)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 p-0.5 rounded hover:bg-gray-100 transition-colors"
                  aria-label={showPassword ? 'Ocultar senha' : 'Mostrar senha'}
                >
                  <EyeIcon open={showPassword} />
                </button>
              </div>
              {(senhaError || capsLockOn) && (
                <p id="senha-help" className={`mt-1.5 text-xs ${senhaError ? 'text-red-600' : 'text-amber-600'}`}>
                  {senhaError || 'Caps Lock ativado'}
                </p>
              )}
            </div>

            {loginError && (
              <div role="alert" className="flex items-center gap-2 p-3 bg-red-50 border border-red-200 rounded-lg">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#dc2626" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="flex-shrink-0">
                  <circle cx="12" cy="12" r="10" />
                  <line x1="12" y1="8" x2="12" y2="12" />
                  <line x1="12" y1="16" x2="12.01" y2="16" />
                </svg>
                <p className="text-sm text-red-700">{loginError}</p>
              </div>
            )}

            <button
              type="submit"
              disabled={mutation.isPending}
              className="w-full rounded-lg bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-indigo-700 active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-60 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
            >
              {mutation.isPending ? (
                <span className="flex items-center justify-center gap-2">
                  <svg className="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
                  </svg>
                  Entrando…
                </span>
              ) : 'Entrar'}
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}
