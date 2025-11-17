import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

export default function Login() {
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState('')
    const [isLoading, setIsLoading] = useState(false)

    const { login } = useAuth()
    const navigate = useNavigate()

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setError('')
        setIsLoading(true)

        try {
            await login(email, password)
            navigate('/')
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Invalid email or password')
        } finally {
            setIsLoading(false)
        }
    }

    return (
        <div className="min-h-screen flex items-center justify-center bg-slate-950 py-12 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
            {/* Animated gradient blobs */}
            <div className="absolute inset-0 overflow-hidden">
                {/* Blob 1 - Blue */}
                <div
                    className="absolute top-0 -left-20 w-[600px] h-[600px] rounded-full blur-3xl opacity-30"
                    style={{
                        background: 'radial-gradient(circle, rgba(59,130,246,0.6) 0%, rgba(37,99,235,0.3) 50%, transparent 70%)',
                        animation: 'gradient-shift 20s ease-in-out infinite'
                    }}
                ></div>

                {/* Blob 2 - Purple */}
                <div
                    className="absolute top-1/4 right-0 w-[500px] h-[500px] rounded-full blur-3xl opacity-40"
                    style={{
                        background: 'radial-gradient(circle, rgba(139,92,246,0.7) 0%, rgba(109,40,217,0.4) 50%, transparent 70%)',
                        animation: 'gradient-shift 18s ease-in-out infinite reverse'
                    }}
                ></div>

                {/* Blob 3 - Cyan */}
                <div
                    className="absolute bottom-0 left-1/3 w-[550px] h-[550px] rounded-full blur-3xl opacity-30"
                    style={{
                        background: 'radial-gradient(circle, rgba(34,211,238,0.5) 0%, rgba(6,182,212,0.3) 50%, transparent 70%)',
                        animation: 'gradient-shift 22s ease-in-out infinite'
                    }}
                ></div>

                {/* Blob 4 - Pink */}
                <div
                    className="absolute bottom-1/4 right-1/4 w-[450px] h-[450px] rounded-full blur-3xl opacity-25"
                    style={{
                        background: 'radial-gradient(circle, rgba(236,72,153,0.6) 0%, rgba(219,39,119,0.3) 50%, transparent 70%)',
                        animation: 'gradient-shift 16s ease-in-out infinite reverse'
                    }}
                ></div>

                {/* Floating geometric shapes */}
                <div
                    className="absolute top-20 left-20 w-32 h-32 border-2 border-blue-500/20 rounded-lg"
                    style={{ animation: 'float 8s ease-in-out infinite' }}
                ></div>
                <div
                    className="absolute bottom-40 right-32 w-24 h-24 border-2 border-purple-500/20 rounded-full"
                    style={{ animation: 'float 10s ease-in-out infinite reverse' }}
                ></div>
                <div
                    className="absolute top-1/2 right-20 w-20 h-20 border-2 border-cyan-500/20"
                    style={{
                        animation: 'float 12s ease-in-out infinite',
                        transform: 'rotate(45deg)'
                    }}
                ></div>
            </div>

            <div className="max-w-md w-full space-y-8 relative z-10">
                {/* Logo with glow effect */}
                <div className="text-center">
                    <div
                        className="mx-auto w-20 h-20 bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 rounded-3xl flex items-center justify-center shadow-2xl mb-8 relative"
                        style={{ animation: 'pulse-glow 3s ease-in-out infinite' }}
                    >
                        <div className="absolute inset-0 bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 rounded-3xl blur-xl opacity-50"></div>
                        <svg className="w-10 h-10 text-white relative z-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                        </svg>
                    </div>

                    <h2 className="text-5xl font-extrabold mb-4">
                        <span className="bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent animate-gradient">
                            Welcome Back
                        </span>
                    </h2>
                    <p className="mt-3 text-lg text-slate-300">
                        Sign in to access your dashboard
                    </p>
                    <p className="mt-4 text-sm text-slate-300">
                        Don't have an account?{' '}
                        <Link
                            to="/register"
                            className="font-semibold text-transparent bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text hover:from-blue-300 hover:to-purple-300 transition-all"
                        >
                            Sign up →
                        </Link>
                    </p>
                </div>

                {/* Login form with glass morphism */}
                <div className="card backdrop-blur-xl bg-slate-900/70 border-slate-700/50 shadow-2xl">
                    <form className="space-y-6" onSubmit={handleSubmit}>
                        {error && (
                            <div className="rounded-xl bg-red-500/10 border border-red-500/30 p-4 backdrop-blur-sm animate-slide-in">
                                <div className="flex items-center gap-3">
                                    <svg className="w-5 h-5 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                    <p className="text-sm text-red-300 font-medium">{error}</p>
                                </div>
                            </div>
                        )}

                        <div className="space-y-5">
                            <div className="group">
                                <label htmlFor="email" className="block text-sm font-semibold text-slate-200 mb-2">
                                    Email Address
                                </label>
                                <div className="relative">
                                    <input
                                        id="email"
                                        name="email"
                                        type="email"
                                        required
                                        value={email}
                                        onChange={(e) => setEmail(e.target.value)}
                                        className="input pl-11"
                                        placeholder="you@company.com"
                                    />
                                    <svg className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400 group-focus-within:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207" />
                                    </svg>
                                </div>
                            </div>

                            <div className="group">
                                <label htmlFor="password" className="block text-sm font-semibold text-slate-200 mb-2">
                                    Password
                                </label>
                                <div className="relative">
                                    <input
                                        id="password"
                                        name="password"
                                        type="password"
                                        required
                                        value={password}
                                        onChange={(e) => setPassword(e.target.value)}
                                        className="input pl-11"
                                        placeholder="••••••••••"
                                    />
                                    <svg className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400 group-focus-within:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                                    </svg>
                                </div>
                            </div>
                        </div>

                        <button
                            type="submit"
                            disabled={isLoading}
                            className="w-full relative group overflow-hidden btn-primary py-4 text-base font-bold disabled:opacity-50 disabled:cursor-not-allowed transform transition-all duration-200 hover:scale-[1.02] active:scale-[0.98] border-radius:25px"
                        >
                            <span className="relative z-10">
                                {isLoading ? (
                                    <span className="flex items-center justify-center gap-2">
                                        <svg className="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                        </svg>
                                        Signing in...
                                    </span>
                                ) : (
                                    'Sign In'
                                )}
                            </span>
                            <div className="absolute inset-0 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                        </button>

                        <div className="mt-6 text-center">
                            <a href="#" className="text-sm text-slate-300 hover:text-blue-400 transition-colors">
                                Forgot password?
                            </a>
                        </div>
                    </form>

                    {/* Trust indicators */}
                    <div className="flex items-center justify-center gap-8 text-xs text-slate-300 mt-6">
                        <div className="flex items-center gap-2">
                            <svg className="w-4 h-4 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                            </svg>
                            <span>Secure Login</span>
                        </div>
                        <div className="flex items-center gap-2">
                            <svg className="w-4 h-4 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clipRule="evenodd" />
                            </svg>
                            <span>256-bit Encryption</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}
