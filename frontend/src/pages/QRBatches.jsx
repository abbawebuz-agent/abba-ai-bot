import { useEffect, useState } from 'react'
import { QrCode } from 'lucide-react'
import api from '../api/client'

export default function QRBatches() {
  const [batches, setBatches] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('qr-batches/').then(r => {
      setBatches(r.data.results || r.data)
      setLoading(false)
    }).catch(() => setLoading(false))
  }, [])

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">QR Kodlar</h1>
        <p className="text-[#888] text-sm mt-1">{batches.length} ta batch</p>
      </div>

      {loading ? (
        <div className="flex justify-center py-20">
          <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : (
        <div className="bg-[#161616] border border-[#2a2a2a] rounded-2xl overflow-hidden">
          <table className="w-full">
            <thead>
              <tr className="border-b border-[#2a2a2a]">
                <th className="px-4 py-3 text-left text-xs text-[#555] font-medium uppercase">Batch nomi</th>
                <th className="px-4 py-3 text-left text-xs text-[#555] font-medium uppercase">Do'kon</th>
                <th className="px-4 py-3 text-left text-xs text-[#555] font-medium uppercase">Jami</th>
                <th className="px-4 py-3 text-left text-xs text-[#555] font-medium uppercase">Faollashtirilgan</th>
                <th className="px-4 py-3 text-left text-xs text-[#555] font-medium uppercase hidden md:table-cell">Sana</th>
              </tr>
            </thead>
            <tbody>
              {batches.map(b => {
                const pct = b.total_codes ? Math.round((b.activated_count / b.total_codes) * 100) : 0
                return (
                  <tr key={b.id} className="border-b border-[#1e1e1e] hover:bg-[#1a1a1a] transition-colors">
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-2">
                        <QrCode size={16} className="text-indigo-400" />
                        <span className="text-white text-sm font-medium">{b.name || `Batch #${b.id}`}</span>
                      </div>
                    </td>
                    <td className="px-4 py-3 text-sm text-[#888]">{b.store_name || '—'}</td>
                    <td className="px-4 py-3 text-sm text-[#888]">{b.total_codes}</td>
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-3">
                        <div className="flex-1 bg-[#2a2a2a] rounded-full h-1.5 max-w-20">
                          <div className="h-1.5 rounded-full bg-indigo-500" style={{ width: `${pct}%` }} />
                        </div>
                        <span className="text-xs text-[#888]">{b.activated_count}/{b.total_codes}</span>
                      </div>
                    </td>
                    <td className="px-4 py-3 text-xs text-[#555] hidden md:table-cell">{b.created_at?.slice(0, 10)}</td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
