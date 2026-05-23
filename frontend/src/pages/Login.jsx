import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

export default function Login() {
  const [form, setForm] = useState({ username: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  async function submit(e) {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const res = await axios.post('/api/v2/auth/login/', form)
      localStorage.setItem('access', res.data.access)
      localStorage.setItem('refresh', res.data.refresh)
      navigate('/')
    } catch {
      setError("Login yoki parol noto'g'ri")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-[#0d0d0d] flex items-center justify-center p-4">
      <div className="w-full max-w-sm">
        <div className="text-center mb-8">
          <div className="w-14 h-14 rounded-2xl bg-indigo-600 flex items-center justify-center text-white font-bold text-2xl mx-auto mb-4">J</div>
          <h1 className="text-2xl font-bold text-white">JIP Admin</h1>
          <p className="text-[#888] text-sm mt-1">Tizimga kirish</p>
        </div>
        <form onSubmit={submit} className="bg-[#161616] border border-[#2a2a2a] rounded-2xl p-6 space-y-4">
          {error && <div className="bg-red-900/30 border border-red-800 text-red-400 text-sm rounded-lg px-4 py-3">{error}</div>}
          <div>
            <label className="text-[#888] text-sm mb-1.5 block">Login</label>
            <input
              type="text"
              value={form.username}
              onChange={e => setForm({ ...form, username: e.target.value })}
              className="w-full bg-[#1e1e1e] border border-[#2a2a2a] rounded-lg px-4 py-2.5 text-white text-sm focus:outline-none focus:border-indigo-500 transition-colors"
              placeholder="admin"
              required
            />
          </div>
          <div>
            <label className="text-[#888] text-sm mb-1.5 block">Parol</label>
            <input
              type="password"
              value={form.password}
              onChange={e => setForm({ ...form, password: e.target.value })}
              className="w-full bg-[#1e1e1e] border border-[#2a2a2a] rounded-lg px-4 py-2.5 text-white text-sm focus:outline-none focus:border-indigo-500 transition-colors"
              placeholder="••••••••"
              required
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white rounded-lg py-2.5 text-sm font-medium transition-colors"
          >
            {loading ? 'Kirish...' : 'Kirish'}
          </button>
        </form>
      </div>
    </div>
  )
}
