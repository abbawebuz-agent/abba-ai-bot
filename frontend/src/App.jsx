import { Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Users from './pages/Users'
import Sellers from './pages/Sellers'
import QRBatches from './pages/QRBatches'

function PrivateRoute({ children }) {
  return localStorage.getItem('access') ? children : <Navigate to="/login" replace />
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/" element={<PrivateRoute><Layout /></PrivateRoute>}>
        <Route index element={<Dashboard />} />
        <Route path="users" element={<Users />} />
        <Route path="sellers" element={<Sellers />} />
        <Route path="qr" element={<QRBatches />} />
      </Route>
    </Routes>
  )
}
