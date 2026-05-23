import axios from 'axios'

const api = axios.create({ baseURL: '/api/v2/' })

api.interceptors.request.use(cfg => {
  const token = localStorage.getItem('access')
  if (token) cfg.headers.Authorization = `Bearer ${token}`
  return cfg
})

api.interceptors.response.use(r => r, async err => {
  if (err.response?.status === 401) {
    const refresh = localStorage.getItem('refresh')
    if (refresh) {
      try {
        const res = await axios.post('/api/v2/auth/refresh/', { refresh })
        localStorage.setItem('access', res.data.access)
        err.config.headers.Authorization = `Bearer ${res.data.access}`
        return axios(err.config)
      } catch {
        localStorage.clear()
        window.location.href = '/panel/login'
      }
    } else {
      window.location.href = '/panel/login'
    }
  }
  return Promise.reject(err)
})

export default api
