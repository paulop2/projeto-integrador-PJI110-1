import axios from 'axios'
import { toast } from 'sonner'
import { authContextRef } from '../contexts/AuthContext'

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor: attach Bearer token from localStorage
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor:
// 1. Pick up X-New-Token header and update token in context + localStorage
// 2. On 401 from non-auth endpoints: clear auth state and redirect to /login
api.interceptors.response.use(
  (response) => {
    // Check for token renewal header
    const newToken = response.headers['x-new-token']
    if (newToken) {
      localStorage.setItem('token', newToken)
      authContextRef.current?.updateToken(newToken)
    }
    return response
  },
  (error) => {
    if (error.response?.status === 401) {
      const url: string = error.config?.url ?? ''
      const isAuthEndpoint =
        url.includes('/auth/login') ||
        url.includes('/auth/forgot-password') ||
        url.includes('/auth/reset-password')

      if (!isAuthEndpoint) {
        // Clear auth state
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        authContextRef.current?.logout()
        // Redirect outside React tree — window.location is correct here
        window.location.href = '/login'
      }
    }
    if (error.response?.status !== 401) {
      const msg = error.response?.data?.detail || 'Erro no servidor. Tente novamente em instantes.'
      toast.error(msg)
    }
    return Promise.reject(error)
  },
)
