import { useEffect, useState } from 'react'
import { createBrowserRouter, RouterProvider, Link, Outlet } from 'react-router-dom'
import { api } from './services/api'

// Layout raiz — será expandido nas fases seguintes
function Root() {
  return (
    <div>
      <nav>
        <Link to="/">Início</Link>
      </nav>
      <Outlet />
    </div>
  )
}

// Página inicial com verificação de CORS
function HomePage() {
  const [backendStatus, setBackendStatus] = useState<string>('verificando...')

  useEffect(() => {
    api
      .get('/health')
      .then((res) => setBackendStatus(JSON.stringify(res.data)))
      .catch((err) => setBackendStatus(`Erro: ${err.message}`))
  }, [])

  return (
    <div>
      <h1>Sistema Escolar</h1>
      <p>Backend: {backendStatus}</p>
    </div>
  )
}

// Usar createBrowserRouter (data API) — NÃO usar BrowserRouter legado
export const router = createBrowserRouter([
  {
    path: '/',
    element: <Root />,
    children: [
      {
        index: true,
        element: <HomePage />,
      },
    ],
  },
])

export default function App() {
  return <RouterProvider router={router} />
}
