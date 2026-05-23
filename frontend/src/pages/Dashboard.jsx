import { useEffect, useState } from 'react'
import { AreaChart, Area, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'
import { Users, QrCode, Clock, CheckCircle, Activity, TrendingUp } from 'lucide-react'
import api from '../api/client'

function StatCard({ icon: Icon, label, value, color, sub }) {
  return (
    <div className="bg-[#161616] border border-[#2a2a2a] rounded-2xl p-5 hover:border-[#3a3a3a] transition-all">
      <div className="flex items-start justify-between mb-4">
        <div className={`w-10 h-10 rounded-xl ${color} flex items-center justify-center`}>
          <Icon size={20} />
        </div>
      </div>
      <div className="text-3xl font-bold text-white mb-1">{value?.toLocaleString() ?? '—'}</div>
      <div className="text-[#888] text-sm">{label}</div>
      {sub && <div className="text-[#555] text-xs mt-1">{sub}</div>}
    </div>
  )
}

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null
  return (
    <div className="bg-[#1e1e1e] border border-[#333] rounded-lg px-3 py-2 text-sm">
      <div className="text-[#888] text-xs mb-1">{label}</div>
      {payload.map((p, i) => (
        <div key={i} style={{ color: p.color }}>{p.value}</div>
      ))}
    </div>
  )
}

export default function Dashboard() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('dashboard/').then(r => {
      setStats(r.data)
      setLoading(false)
    }).catch(() => setLoading(false))
  }, [])

  if (loading) return (
    <div className="flex items-center justify-center h-64">
      <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
    </div>
  )

  const cards = [
    { icon: Users, label: "Jami foydalanuvchilar", value: stats?.total_users, color: "bg-indigo-600/20 text-indigo-400" },
    { icon: Activity, label: "Santeniklar", value: stats?.santeniklar, color: "bg-amber-600/20 text-amber-400" },
    { icon: CheckCircle, label: "Tasdiqlangan sotuvchilar", value: stats?.sotuvchilar, color: "bg-emerald-600/20 text-emerald-400" },
    { icon: Clock, label: "Kutilayotgan arizalar", value: stats?.pending_sellers, color: "bg-rose-600/20 text-rose-400", sub: stats?.pending_sellers > 0 ? 'Tasdiqlash kerak!' : '' },
    { icon: QrCode, label: "Jami QR kodlar", value: stats?.total_qr, color: "bg-purple-600/20 text-purple-400" },
    { icon: TrendingUp, label: "Bugun skanerlar", value: stats?.today_scans, color: "bg-cyan-600/20 text-cyan-400", sub: `Hafta: ${stats?.week_scans}` },
  ]

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-white">Dashboard</h1>
        <p className="text-[#888] text-sm mt-1">JIP loyalty tizimi statistikasi</p>
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
        {cards.map((c, i) => <StatCard key={i} {...c} />)}
      </div>

      <div className="grid lg:grid-cols-2 gap-4">
        <div className="bg-[#161616] border border-[#2a2a2a] rounded-2xl p-5">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-white font-semibold">QR Skanerlar (7 kun)</h2>
          </div>
          <ResponsiveContainer width="100%" height={200}>
            <AreaChart data={stats?.scans_chart}>
              <defs>
                <linearGradient id="scanGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                </linearGradient>
              </defs>
              <XAxis dataKey="date" tick={{ fill: '#555', fontSize: 11 }} tickFormatter={d => d.slice(5)} />
              <YAxis tick={{ fill: '#555', fontSize: 11 }} />
              <Tooltip content={<CustomTooltip />} />
              <Area type="monotone" dataKey="scans" stroke="#6366f1" fill="url(#scanGrad)" strokeWidth={2} />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-[#161616] border border-[#2a2a2a] rounded-2xl p-5">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-white font-semibold">Yangi foydalanuvchilar (30 kun)</h2>
          </div>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={stats?.users_chart?.filter((_, i) => i % 3 === 0)}>
              <XAxis dataKey="date" tick={{ fill: '#555', fontSize: 11 }} tickFormatter={d => d.slice(5)} />
              <YAxis tick={{ fill: '#555', fontSize: 11 }} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="users" fill="#6366f1" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}
