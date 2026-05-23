import { useEffect, useState } from 'react'
import { CheckCircle, XCircle, MapPin, Phone, Clock, ChevronLeft, ChevronRight } from 'lucide-react'
import api from '../api/client'

export default function Sellers() {
  const [sellers, setSellers] = useState([])
  const [loading, setLoading] = useState(true)
  const [page, setPage] = useState(1)
  const [total, setTotal] = useState(0)
  const [acting, setActing] = useState({})

  function load(p = page) {
    setLoading(true)
    api.get(`users/?seller_approved=false&user_type=sotuvchi&page=${p}`)
      .then(r => {
        setSellers(r.data.results || r.data)
        setTotal(r.data.count || r.data.length)
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }

  useEffect(() => { load(page) }, [page])

  async function action(id, type) {
    setActing(a => ({ ...a, [id]: type }))
    try {
      await api.post(`users/${id}/${type}/`)
      load(page)
    } finally {
      setActing(a => { const n = { ...a }; delete n[id]; return n })
    }
  }

  const totalPages = Math.ceil(total / 50) || 1

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">Zaproslar</h1>
        <p className="text-[#888] text-sm mt-1">
          Tasdiqlanmagan sotuvchi arizalari — {total} ta
        </p>
      </div>

      {loading ? (
        <div className="flex justify-center py-20">
          <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : sellers.length === 0 ? (
        <div className="bg-[#161616] border border-[#2a2a2a] rounded-2xl p-12 text-center">
          <CheckCircle size={40} className="text-emerald-500 mx-auto mb-3" />
          <p className="text-white font-medium">Barcha arizalar ko'rib chiqilgan</p>
          <p className="text-[#555] text-sm mt-1">Yangi arizalar kelganda bu yerda ko'rinadi</p>
        </div>
      ) : (
        <>
          <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-4 mb-4">
            {sellers.map(s => (
              <div key={s.id} className="bg-[#161616] border border-[#2a2a2a] rounded-2xl p-5 hover:border-[#3a3a3a] transition-all">
                <div className="flex items-start justify-between mb-4">
                  <div className="w-11 h-11 rounded-xl bg-indigo-600/20 flex items-center justify-center text-indigo-400 font-semibold text-lg">
                    {(s.first_name || s.username || '?')[0].toUpperCase()}
                  </div>
                  <div className="flex items-center gap-1 text-xs text-[#555]">
                    <Clock size={12} />
                    {s.created_at?.slice(0, 10)}
                  </div>
                </div>
                <div className="mb-4">
                  <div className="font-semibold text-white">{s.first_name || 'Nomsiz'} {s.last_name || ''}</div>
                  {s.username && <div className="text-[#555] text-sm">@{s.username}</div>}
                </div>
                <div className="space-y-2 mb-5">
                  {s.phone_number && (
                    <div className="flex items-center gap-2 text-sm text-[#888]">
                      <Phone size={13} className="text-[#555]" />
                      {s.phone_number}
                    </div>
                  )}
                  {s.region_name && (
                    <div className="flex items-center gap-2 text-sm text-[#888]">
                      <MapPin size={13} className="text-[#555]" />
                      {s.region_name}{s.district_name ? `, ${s.district_name}` : ''}
                    </div>
                  )}
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => action(s.id, 'approve')}
                    disabled={!!acting[s.id]}
                    className="flex-1 flex items-center justify-center gap-2 py-2 bg-emerald-900/30 border border-emerald-800 text-emerald-400 rounded-lg text-sm hover:bg-emerald-900/50 disabled:opacity-50 transition-colors"
                  >
                    {acting[s.id] === 'approve'
                      ? <div className="w-4 h-4 border-2 border-emerald-400 border-t-transparent rounded-full animate-spin" />
                      : <><CheckCircle size={15} /> Tasdiqlash</>
                    }
                  </button>
                  <button
                    onClick={() => action(s.id, 'reject')}
                    disabled={!!acting[s.id]}
                    className="flex-1 flex items-center justify-center gap-2 py-2 bg-rose-900/30 border border-rose-800 text-rose-400 rounded-lg text-sm hover:bg-rose-900/50 disabled:opacity-50 transition-colors"
                  >
                    {acting[s.id] === 'reject'
                      ? <div className="w-4 h-4 border-2 border-rose-400 border-t-transparent rounded-full animate-spin" />
                      : <><XCircle size={15} /> Rad etish</>
                    }
                  </button>
                </div>
              </div>
            ))}
          </div>

          {totalPages > 1 && (
            <div className="flex items-center justify-between px-1">
              <span className="text-[#555] text-sm">{total} ta ariza</span>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setPage(p => Math.max(1, p - 1))}
                  disabled={page === 1}
                  className="p-1.5 rounded-lg text-[#555] hover:text-white hover:bg-[#2a2a2a] disabled:opacity-30 transition-colors"
                >
                  <ChevronLeft size={18} />
                </button>
                <span className="text-sm text-[#888] px-2">{page} / {totalPages}</span>
                <button
                  onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                  disabled={page === totalPages}
                  className="p-1.5 rounded-lg text-[#555] hover:text-white hover:bg-[#2a2a2a] disabled:opacity-30 transition-colors"
                >
                  <ChevronRight size={18} />
                </button>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  )
}
