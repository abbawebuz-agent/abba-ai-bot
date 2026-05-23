import { useEffect, useState } from 'react'
import { CheckCircle, XCircle, MapPin, Phone, Clock } from 'lucide-react'
import api from '../api/client'

export default function Sellers() {
  const [sellers, setSellers] = useState([])
  const [loading, setLoading] = useState(true)

  function load() {
    setLoading(true)
    api.get('users/?seller_approved=false&user_type=sotuvchi').then(r => {
      setSellers(r.data.results || r.data)
      setLoading(false)
    }).catch(() => setLoading(false))
  }

  useEffect(() => { load() }, [])

  async function action(id, type) {
    await api.post(`users/${id}/${type}/`)
    load()
  }

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">Zaproslar</h1>
        <p className="text-[#888] text-sm mt-1">Tasdiqlanmagan sotuvchi arizalari — {sellers.length} ta</p>
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
        <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-4">
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
                  className="flex-1 flex items-center justify-center gap-2 py-2 bg-emerald-900/30 border border-emerald-800 text-emerald-400 rounded-lg text-sm hover:bg-emerald-900/50 transition-colors"
                >
                  <CheckCircle size={15} /> Tasdiqlash
                </button>
                <button
                  onClick={() => action(s.id, 'reject')}
                  className="flex-1 flex items-center justify-center gap-2 py-2 bg-rose-900/30 border border-rose-800 text-rose-400 rounded-lg text-sm hover:bg-rose-900/50 transition-colors"
                >
                  <XCircle size={15} /> Rad etish
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
