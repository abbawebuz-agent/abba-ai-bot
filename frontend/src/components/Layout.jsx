import { Outlet, NavLink, useNavigate } from 'react-router-dom'
import { LayoutDashboard, Users, ShoppingCart, QrCode, LogOut, Menu, X, Settings } from 'lucide-react'
import { useState } from 'react'

const nav = [
  { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/users', icon: Users, label: 'Foydalanuvchilar' },
  { to: '/sellers', icon: ShoppingCart, label: 'Zaproslar' },
  { to: '/qr', icon: QrCode, label: 'QR Kodlar' },
]

export default function Layout() {
  const navigate = useNavigate()
  const [open, setOpen] = useState(false)

  function logout() {
    localStorage.clear()
    navigate('/login')
  }

  return (
    <div className="flex h-screen bg-[#0d0d0d]">
      {/* Sidebar */}
      <aside className={`fixed inset-y-0 left-0 z-50 w-64 bg-[#111] border-r border-[#222] flex flex-col transition-transform lg:translate-x-0 ${open ? 'translate-x-0' : '-translate-x-full'}`}>
        <div className="flex items-center gap-3 px-6 py-5 border-b border-[#222]">
          <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center text-white font-bold text-sm">J</div>
          <span className="font-semibold text-white text-lg">JIP Admin</span>
        </div>
        <nav className="flex-1 px-3 py-4 space-y-1">
          {nav.map(({ to, icon: Icon, label }) => (
            <NavLink key={to} to={to} end={to === '/'} onClick={() => setOpen(false)}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-all ${
                  isActive ? 'bg-indigo-600/20 text-indigo-400 font-medium' : 'text-[#888] hover:text-white hover:bg-[#1e1e1e]'
                }`
              }>
              <Icon size={18} />
              {label}
            </NavLink>
          ))}
        </nav>
        <div className="px-3 py-4 border-t border-[#222] space-y-1">
          <a
            href="/admin/"
            className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-[#888] hover:text-indigo-400 hover:bg-indigo-900/10 transition-all w-full"
          >
            <Settings size={18} />
            Django Admin
          </a>
          <button onClick={logout} className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-[#888] hover:text-red-400 hover:bg-red-900/10 transition-all w-full">
            <LogOut size={18} />
            Chiqish
          </button>
        </div>
      </aside>

      {/* Mobile overlay */}
      {open && <div className="fixed inset-0 bg-black/60 z-40 lg:hidden" onClick={() => setOpen(false)} />}

      {/* Main */}
      <div className="flex-1 flex flex-col lg:ml-64 min-h-screen overflow-hidden">
        <header className="h-14 border-b border-[#222] flex items-center px-6 lg:hidden">
          <button onClick={() => setOpen(!open)} className="text-[#888] hover:text-white">
            {open ? <X size={22} /> : <Menu size={22} />}
          </button>
        </header>
        <main className="flex-1 overflow-y-auto p-6">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
