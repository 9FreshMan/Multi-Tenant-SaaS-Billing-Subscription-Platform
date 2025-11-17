import { Outlet, Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import {
    LayoutDashboard,
    CreditCard,
    Receipt,
    BarChart3,
    Settings,
    LogOut,
    Menu
} from 'lucide-react'
import { useState } from 'react'

export default function Layout() {
    const { user, logout } = useAuth()
    const navigate = useNavigate()
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

    const handleLogout = () => {
        logout()
        navigate('/login')
    }

    const navigation = [
        { name: 'Dashboard', href: '/', icon: LayoutDashboard },
        { name: 'Subscriptions', href: '/subscriptions', icon: CreditCard },
        { name: 'Invoices', href: '/invoices', icon: Receipt },
        { name: 'Usage & Analytics', href: '/usage', icon: BarChart3 },
        { name: 'Settings', href: '/settings', icon: Settings },
    ]

    return (
        <div className="min-h-screen bg-slate-950">
            {/* Sidebar */}
            <div className="hidden lg:fixed lg:inset-y-0 lg:flex lg:w-64 lg:flex-col">
                <div className="flex flex-col flex-grow bg-slate-900 border-r border-slate-800 pt-5 shadow-2xl">
                    <div className="flex items-center flex-shrink-0 px-6 mb-8">
                        <div className="flex items-center gap-3">
                            <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center shadow-lg shadow-blue-500/30">
                                <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                                </svg>
                            </div>
                            <div>
                                <h1 className="text-lg font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">SaaS Billing</h1>
                                <p className="text-xs text-slate-500">Enterprise</p>
                            </div>
                        </div>
                    </div>
                    <div className="mt-2 flex-1 flex flex-col">
                        <nav className="flex-1 px-3 space-y-1">
                            {navigation.map((item) => (
                                <Link
                                    key={item.name}
                                    to={item.href}
                                    className="group flex items-center px-3 py-3 text-sm font-medium rounded-lg text-slate-300 hover:text-white hover:bg-slate-800/70 transition-all duration-200 border border-transparent hover:border-slate-700"
                                >
                                    <item.icon className="mr-3 h-5 w-5 text-slate-400 group-hover:text-blue-400 transition-colors" />
                                    <span className="font-semibold">{item.name}</span>
                                </Link>
                            ))}
                        </nav>
                    </div>
                    <div className="flex-shrink-0 flex border-t border-slate-700 p-4 bg-slate-800/30">
                        <div className="flex items-center w-full">
                            <div className="flex-shrink-0 w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold shadow-lg shadow-blue-500/30">
                                {user?.first_name?.[0]}{user?.last_name?.[0]}
                            </div>
                            <div className="flex-1 ml-3">
                                <p className="text-sm font-semibold text-slate-100">
                                    {user?.first_name} {user?.last_name}
                                </p>
                                <p className="text-xs text-slate-400 truncate">{user?.email}</p>
                            </div>
                            <button
                                onClick={handleLogout}
                                className="ml-2 p-2 text-slate-300 hover:text-red-400 hover:bg-slate-800 rounded-lg transition-all duration-200"
                                title="Logout"
                            >
                                <LogOut className="h-5 w-5" />
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            {/* Mobile header */}
            <div className="lg:hidden sticky top-0 z-10 bg-slate-900 border-b border-slate-800 backdrop-blur-lg bg-opacity-95">
                <div className="flex items-center justify-between px-4 py-3">
                    <div className="flex items-center gap-2">
                        <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                            <svg className="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                            </svg>
                        </div>
                        <h1 className="text-lg font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">SaaS Billing</h1>
                    </div>
                    <button
                        onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                        className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800"
                    >
                        <Menu className="h-6 w-6" />
                    </button>
                </div>
            </div>

            {/* Main content */}
            <div className="lg:pl-64 flex flex-col flex-1">
                <main className="flex-1 p-6 max-w-7xl mx-auto w-full">
                    <Outlet />
                </main>
            </div>
        </div>
    )
}
