import { useState } from 'react'
import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar'
import { UserMenu } from '../UserMenu'

export default function AdminLayout() {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)
  const [mobileOpen, setMobileOpen] = useState(false)

  return (
    <div className="flex h-screen overflow-hidden bg-gray-50">
      {/* Desktop sidebar — oculta abaixo do breakpoint md (768px) */}
      <div className="hidden md:flex">
        <Sidebar
          collapsed={sidebarCollapsed}
          onToggle={() => setSidebarCollapsed((prev) => !prev)}
        />
      </div>

      {/* Mobile overlay drawer — visível apenas quando mobileOpen === true */}
      {mobileOpen && (
        <>
          {/* Backdrop semitransparente — cobre o conteúdo principal */}
          <div
            className="fixed inset-0 bg-black/50 z-40 md:hidden"
            onClick={() => setMobileOpen(false)}
            aria-hidden="true"
          />
          {/* Drawer panel — sidebar completa não colapsada */}
          <div
            id="admin-mobile-drawer"
            className="fixed inset-y-0 left-0 z-50 md:hidden"
          >
            <Sidebar
              collapsed={false}
              onToggle={() => setMobileOpen(false)}
            />
          </div>
        </>
      )}

      {/* Coluna direita: header + main */}
      <div className="flex flex-col flex-1 min-w-0 overflow-hidden">
        {/* Header fixo h-16 */}
        <header className="h-16 bg-white border-b border-gray-200 shadow-sm flex items-center justify-between px-4 flex-shrink-0 z-30">
          {/* Hamburger para mobile — oculto no desktop (md+) */}
          <button
            onClick={() => setMobileOpen(true)}
            className="md:hidden p-2 rounded-md text-gray-500 hover:bg-gray-100 hover:text-gray-700 transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500"
            aria-label="Abrir menu"
            aria-expanded={mobileOpen}
            aria-controls="admin-mobile-drawer"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <line x1="3" y1="6" x2="21" y2="6" />
              <line x1="3" y1="12" x2="21" y2="12" />
              <line x1="3" y1="18" x2="21" y2="18" />
            </svg>
          </button>

          {/* Logo — visível apenas no mobile (desktop tem logo na sidebar) */}
          <span className="md:hidden text-xl font-semibold text-indigo-600">EscolaApp</span>
          {/* Spacer no desktop */}
          <span className="hidden md:block" />

          {/* UserMenu — avatar + dropdown */}
          <UserMenu />
        </header>

        {/* Main content area */}
        <main id="conteudo-principal" className="flex-1 overflow-y-auto">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
