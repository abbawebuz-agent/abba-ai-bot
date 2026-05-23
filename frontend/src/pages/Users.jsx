import { useEffect, useState } from 'react'
import { Search, Trash2, ChevronLeft, ChevronRight } from 'lucide-react'
import api from '../api/client'

function UserTypeBadge({ type, approved }) {
  if (type === 'santenik') return <span className="px-2 py-0.5 rounded-md text-xs bg-amber-900/40 text-amber-400">Santenik</span>
  if (type === 'sotuvchi' && approved) return <span className="px-2 py-0.5 rounded-md text-xs bg-blue-900/40 text-blue-400">Sotuvchi</span>
  if (type === 'sotuvchi') return <span className="px-2 py-0.5 rounded-md text-xs bg-rose-900/40 text-rose-400">Kutilmoqda</span>
  return <span className="px-2 py-0.5 rounded-md text-xs bg-[#2a2a2a] text-[#888]">—</span>
}

export default function Users() {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [filter, setFilter] = useState('')
  const [selected, setSelected] = useState([])
  const [page, setPage] = useState(1)
  const [total, setTotal] = useState(0)

  function load() {
    setLoading(true)
    const params = new URLSearchParams()
    if (search) params.set('search', search)
    if (filter) params.set('user_type', filter)
    params.set('page', page)
    api.get(`users/?${params}`).then(r => {
      setUsers(r.data.results || r.data)
      setTotal(r.data.count || r.data.length)
      setLoading(false)
    }).catch(() => setLoading(false))
  }

  useEffect(() => { load() }, [search, filter, page])

  function toggleSelect(id) {
    setSelected(s => s.includes(id) ? s.filter(x => x !== id) : [...s, id])
  }

  function toggleAll() {
    setSelected(s => s.length === users.length ? [] : users.map(u => u.id))
  }

  async function deleteSelected() {
    if (!selected.length || !confirm(`${selected.length} ta foydalanuvchini o'chirish?`)) return
    await api.post('users/bulk-delete/', { ids: selected })
    setSelected([])
    load()
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-white">Foydalanuvchilar</h1>
          <p className="text-[#888] text-sm mt-1">Jami: {total}</p>
        </div>
        {selected.length > 0 && (
          <button onClick={deleteSelected} className="flex items-center gap-2 px-4 py-2 bg-red-900/30 border border-red-800 text-red-400 rounded-lg text-sm hover:bg-red-900/50 transition-colors">
            <Trash2 size={16} />
            {selected.length} ta o'chirish
          </button>
        )}
      </div>

      {/* Filters */}
      <div className="flex gap-3 mb-4">
        <div className="relative flex-1 max-w-sm">
          <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-[#555]" />
          <input
            value={search}
            onChange={e => { setSearch(e.target.value); setPage(1) }}
            placeholder="Ism, username, telefon..."
            className="w-full bg-[#161616] border border-[#2a2a2a] rounded-lg pl-9 pr-4 py-2 text-sm text-white focus:outline-none focus:border-indigo-500"
          />
        </div>
        <select
          value={filter}
          onChange={e => { setFilter(e.target.value); setPage(1) }}
          className="bg-[#161616] border border-[#2a2a2a] rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-indigo-500"
        >
          <option value="">Barcha turlar</option>
          <option value="santenik">Santenik</option>
          <option value="sotuvchi">Sotuvchi</option>
        </select>
      </div>

      {/* Table */}
      <div className="bg-[#161616] border border-[#2a2a2a] rounded-2xl overflow-hidden">
        <table className="w-full">
          <thead>
            <tr className="border-b border-[#2a2a2a]">
              <th className="px-4 py-3 text-left">
                <input
                  type="checkbox"
                  checked={selected.length === users.length && users.length > 0}
                  onChange={toggleAll}
                  className="rounded"
                />
              </th>
              <th className="px-4 py-3 text-left text-xs text-[#555] font-medium uppercase">Foydalanuvchi</th>
              <th className="px-4 py-3 text-left text-xs text-[#555] font-medium uppercase hidden md:table-cell">Telefon</th>
              <th className="px-4 py-3 text-left text-xs text-[#555] font-medium uppercase hidden lg:table-cell">Viloyat</th>
              <th className="px-4 py-3 text-left text-xs text-[#555] font-medium uppercase">Tur</th>
              <th className="px-4 py-3 text-left text-xs text-[#555] font-medium uppercase hidden md:table-cell">Sana</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan={6} className="text-center py-12 text-[#555]">
                  <div className="w-6 h-6 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin mx-auto" />
                </td>
              </tr>
            ) : users.length === 0 ? (
              <tr>
                <td colSpan={6} className="text-center py-12 text-[#555]">Foydalanuvchilar topilmadi</td>
              </tr>
            ) : users.map(u => (
              <tr
                key={u.id}
                className={`border-b border-[#1e1e1e] hover:bg-[#1a1a1a] transition-colors ${selected.includes(u.id) ? 'bg-indigo-900/10' : ''}`}
              >
                <td className="px-4 py-3">
                  <input type="checkbox" checked={selected.includes(u.id)} onChange={() => toggleSelect(u.id)} />
                </td>
                <td className="px-4 py-3">
                  <div className="font-medium text-white text-sm">{u.first_name || u.username || 'Nomsiz'}</div>
                  {u.username && <div className="text-[#555] text-xs">@{u.username}</div>}
                </td>
                <td className="px-4 py-3 text-sm text-[#888] hidden md:table-cell">{u.phone_number || '—'}</td>
                <td className="px-4 py-3 text-sm text-[#888] hidden lg:table-cell">{u.region_name || '—'}</td>
                <td className="px-4 py-3">
                  <UserTypeBadge type={u.user_type} approved={u.seller_approved} />
                </td>
                <td className="px-4 py-3 text-xs text-[#555] hidden md:table-cell">{u.created_at?.slice(0, 10)}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {/* Pagination */}
        <div className="px-4 py-3 border-t border-[#2a2a2a] flex items-center justify-between">
          <span className="text-[#555] text-sm">{total} ta natija</span>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setPage(p => Math.max(1, p - 1))}
              disabled={page === 1}
              className="p-1.5 rounded-lg text-[#555] hover:text-white hover:bg-[#2a2a2a] disabled:opacity-30 transition-colors"
            >
              <ChevronLeft size={18} />
            </button>
            <span className="text-sm text-[#888] px-2">{page} / {Math.ceil(total / 50) || 1}</span>
            <button
              onClick={() => setPage(p => p + 1)}
              disabled={page * 50 >= total}
              className="p-1.5 rounded-lg text-[#555] hover:text-white hover:bg-[#2a2a2a] disabled:opacity-30 transition-colors"
            >
              <ChevronRight size={18} />
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
