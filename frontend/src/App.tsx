import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import Layout from './components/Layout'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Plans from './pages/Plans'
import Subscriptions from './pages/Subscriptions'
import Invoices from './pages/Invoices'
import Usage from './pages/Usage'
import Settings from './pages/Settings'

function PrivateRoute({ children }: { children: React.ReactNode }) {
    const { user, isLoading } = useAuth()

    if (isLoading) {
        return (
            <div className="min-h-screen bg-slate-950 flex items-center justify-center">
                <div className="text-center">
                    <div className="inline-block w-16 h-16 border-4 border-blue-500/30 border-t-blue-500 rounded-full animate-spin mb-4"></div>
                    <p className="text-slate-300 text-lg font-medium">Loading...</p>
                </div>
            </div>
        )
    }

    return user ? <>{children}</> : <Navigate to="/login" />
}

function App() {
    return (
        <BrowserRouter>
            <AuthProvider>
                <Routes>
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />

                    <Route path="/" element={
                        <PrivateRoute>
                            <Layout />
                        </PrivateRoute>
                    }>
                        <Route index element={<Dashboard />} />
                        <Route path="plans" element={<Plans />} />
                        <Route path="subscriptions" element={<Subscriptions />} />
                        <Route path="invoices" element={<Invoices />} />
                        <Route path="usage" element={<Usage />} />
                        <Route path="settings" element={<Settings />} />
                    </Route>
                </Routes>
            </AuthProvider>
        </BrowserRouter>
    )
}

export default App
