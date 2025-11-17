import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { authService } from '../services/auth'

export default function Register() {
    const [formData, setFormData] = useState({
        tenant_name: '',
        tenant_slug: '',
        email: '',
        password: '',
        first_name: '',
        last_name: '',
    })
    const [error, setError] = useState('')
    const [isLoading, setIsLoading] = useState(false)

    const navigate = useNavigate()

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target
        setFormData(prev => ({ ...prev, [name]: value }))

        // Auto-generate slug from company name
        if (name === 'tenant_name') {
            const slug = value.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '')
            setFormData(prev => ({ ...prev, tenant_slug: slug }))
        }
    }

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setError('')
        setIsLoading(true)

        try {
            const response = await authService.register(formData)
            localStorage.setItem('access_token', response.access_token)
            localStorage.setItem('refresh_token', response.refresh_token)
            navigate('/')
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Registration failed')
        } finally {
            setIsLoading(false)
        }
    }

    return (
        <div className="min-h-screen flex items-center justify-center bg-slate-950 py-12 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
            {/* Animated gradient blobs - mirrored from Login */}
            <div className="absolute inset-0 overflow-hidden">
                {/* Blob 1 - Purple */}
                <div
                    className="absolute top-0 right-0 w-[650px] h-[650px] rounded-full blur-3xl opacity-30"
                    style={{
                        background: 'radial-gradient(circle, rgba(139,92,246,0.7) 0%, rgba(109,40,217,0.4) 50%, transparent 70%)',
                        animation: 'gradient-shift 19s ease-in-out infinite'
                    }}
                ></div>

                {/* Blob 2 - Cyan */}
                <div
                    className="absolute bottom-0 left-0 w-[600px] h-[600px] rounded-full blur-3xl opacity-35"
                    style={{
                        background: 'radial-gradient(circle, rgba(34,211,238,0.6) 0%, rgba(6,182,212,0.3) 50%, transparent 70%)',
                        animation: 'gradient-shift 21s ease-in-out infinite reverse'
                    }}
                ></div>

                {/* Blob 3 - Blue */}
                <div
                    className="absolute top-1/3 left-1/4 w-[500px] h-[500px] rounded-full blur-3xl opacity-30"
                    style={{
                        background: 'radial-gradient(circle, rgba(59,130,246,0.6) 0%, rgba(37,99,235,0.3) 50%, transparent 70%)',
                        animation: 'gradient-shift 17s ease-in-out infinite'
                    }}
                ></div>

                {/* Blob 4 - Emerald */}
                <div
                    className="absolute bottom-1/3 right-1/3 w-[480px] h-[480px] rounded-full blur-3xl opacity-25"
                    style={{
                        background: 'radial-gradient(circle, rgba(16,185,129,0.5) 0%, rgba(5,150,105,0.3) 50%, transparent 70%)',
                        animation: 'gradient-shift 23s ease-in-out infinite reverse'
                    }}
                ></div>

                {/* Floating geometric shapes */}
                <div
                    className="absolute top-32 right-24 w-28 h-28 border-2 border-purple-500/20 rounded-full"
                    style={{ animation: 'float 9s ease-in-out infinite' }}
                ></div>
                <div
                    className="absolute bottom-32 left-28 w-24 h-24 border-2 border-cyan-500/20"
                    style={{
                        animation: 'float 11s ease-in-out infinite reverse',
                        transform: 'rotate(45deg)'
                    }}
                ></div>
                <div
                    className="absolute top-1/2 left-16 w-20 h-20 border-2 border-blue-500/20 rounded-lg"
                    style={{ animation: 'float 13s ease-in-out infinite' }}
                ></div>
            </div>

            <div className="max-w-2xl w-full space-y-8 relative z-10">
                {/* Logo with glow effect */}
                <div className="text-center">
                    <div
                        className="mx-auto w-20 h-20 bg-gradient-to-br from-purple-500 via-blue-500 to-cyan-500 rounded-3xl flex items-center justify-center shadow-2xl mb-8 relative"
                        style={{ animation: 'pulse-glow 3s ease-in-out infinite' }}
                    >
                        <div className="absolute inset-0 bg-gradient-to-br from-purple-500 via-blue-500 to-cyan-500 rounded-3xl blur-xl opacity-50"></div>
                        <svg className="w-10 h-10 text-white relative z-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                        </svg>
                    </div>

                    <h2 className="text-5xl font-extrabold mb-4">
                        <span className="bg-gradient-to-r from-purple-400 via-blue-400 to-cyan-400 bg-clip-text text-transparent animate-gradient">
                            Join Us Today
                        </span>
                    </h2>
                    <p className="mt-3 text-lg text-slate-300">
                        Create your account and start your free trial
                    </p>
                    <p className="mt-4 text-sm text-slate-300">
                        Already have an account?{' '}
                        <Link
                            to="/login"
                            className="font-semibold text-transparent bg-gradient-to-r from-purple-400 to-cyan-400 bg-clip-text hover:from-purple-300 hover:to-cyan-300 transition-all"
                        >
                            Sign in →
                        </Link>
                    </p>
                </div>

                {/* Registration form with glass morphism */}
                <div className="card backdrop-blur-xl bg-slate-900/70 border-slate-700/50 shadow-2xl">
                    <form className="space-y-5" onSubmit={handleSubmit}>
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

                        {/* Company Name field with icon */}
                        <div>
                            <label htmlFor="tenant_name" className="block text-sm font-semibold text-slate-200 mb-2">
                                Company Name
                            </label>
                            <div className="relative group">
                                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                    <svg className="w-5 h-5 text-slate-400 group-focus-within:text-purple-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                                    </svg>
                                </div>
                                <input
                                    id="tenant_name"
                                    name="tenant_name"
                                    type="text"
                                    required
                                    value={formData.tenant_name}
                                    onChange={handleChange}
                                    className="input pl-10 focus:ring-2 focus:ring-purple-500/50 transition-all"
                                    placeholder="Acme Corporation"
                                />
                            </div>
                        </div>

                        {/* Company Slug field with icon */}
                        <div>
                            <label htmlFor="tenant_slug" className="block text-sm font-semibold text-slate-200 mb-2">
                                Company Slug
                            </label>
                            <div className="relative group">
                                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                    <svg className="w-5 h-5 text-slate-400 group-focus-within:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                                    </svg>
                                </div>
                                <input
                                    id="tenant_slug"
                                    name="tenant_slug"
                                    type="text"
                                    required
                                    value={formData.tenant_slug}
                                    onChange={handleChange}
                                    className="input pl-10 focus:ring-2 focus:ring-blue-500/50 transition-all"
                                    placeholder="acme-corporation"
                                />
                            </div>
                        </div>

                        {/* Name fields grid with icons */}
                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label htmlFor="first_name" className="block text-sm font-semibold text-slate-200 mb-2">
                                    First Name
                                </label>
                                <div className="relative group">
                                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                        <svg className="w-5 h-5 text-slate-400 group-focus-within:text-cyan-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                                        </svg>
                                    </div>
                                    <input
                                        id="first_name"
                                        name="first_name"
                                        type="text"
                                        required
                                        value={formData.first_name}
                                        onChange={handleChange}
                                        className="input pl-10 focus:ring-2 focus:ring-cyan-500/50 transition-all"
                                        placeholder="John"
                                    />
                                </div>
                            </div>
                            <div>
                                <label htmlFor="last_name" className="block text-sm font-semibold text-slate-200 mb-2">
                                    Last Name
                                </label>
                                <div className="relative group">
                                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                        <svg className="w-5 h-5 text-slate-400 group-focus-within:text-cyan-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                                        </svg>
                                    </div>
                                    <input
                                        id="last_name"
                                        name="last_name"
                                        type="text"
                                        required
                                        value={formData.last_name}
                                        onChange={handleChange}
                                        className="input pl-10 focus:ring-2 focus:ring-cyan-500/50 transition-all"
                                        placeholder="Doe"
                                    />
                                </div>
                            </div>
                        </div>

                        {/* Email field with icon */}
                        <div>
                            <label htmlFor="email" className="block text-sm font-semibold text-slate-200 mb-2">
                                Email Address
                            </label>
                            <div className="relative group">
                                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                    <svg className="w-5 h-5 text-slate-400 group-focus-within:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                                    </svg>
                                </div>
                                <input
                                    id="email"
                                    name="email"
                                    type="email"
                                    required
                                    value={formData.email}
                                    onChange={handleChange}
                                    className="input pl-10 focus:ring-2 focus:ring-blue-500/50 transition-all"
                                    placeholder="john.doe@acme.com"
                                />
                            </div>
                        </div>

                        {/* Password field with icon */}
                        <div>
                            <label htmlFor="password" className="block text-sm font-semibold text-slate-200 mb-2">
                                Password
                            </label>
                            <div className="relative group">
                                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                    <svg className="w-5 h-5 text-slate-400 group-focus-within:text-purple-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                                    </svg>
                                </div>
                                <input
                                    id="password"
                                    name="password"
                                    type="password"
                                    required
                                    minLength={8}
                                    value={formData.password}
                                    onChange={handleChange}
                                    className="input pl-10 focus:ring-2 focus:ring-purple-500/50 transition-all"
                                    placeholder="Minimum 8 characters"
                                />
                            </div>
                        </div>

                        {/* Submit button with gradient hover */}
                        <div className="pt-2">
                            <button
                                type="submit"
                                disabled={isLoading}
                                className="group relative w-full flex justify-center items-center gap-3 py-3.5 px-4 border border-transparent text-base font-semibold rounded-xl text-white bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-[1.02] active:scale-[0.98] shadow-xl hover:shadow-purple-500/25"
                            >
                                <div className="absolute inset-0 bg-gradient-to-r from-purple-400 via-blue-400 to-cyan-400 rounded-xl opacity-0 group-hover:opacity-20 blur transition-opacity"></div>
                                <span className="relative">
                                    {isLoading ? (
                                        <>
                                            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white inline-block" fill="none" viewBox="0 0 24 24">
                                                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                            </svg>
                                            Creating your account...
                                        </>
                                    ) : (
                                        <>
                                            Create Account
                                            <svg className="w-5 h-5 transform group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                                            </svg>
                                        </>
                                    )}
                                </span>
                            </button>
                        </div>

                        {/* Trust indicators */}
                        <div className="pt-4 flex items-center justify-center gap-6 text-xs text-slate-300">
                            <div className="flex items-center gap-2">
                                <svg className="w-4 h-4 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                                    <path fillRule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                                </svg>
                                <span>Free 14-day trial</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <svg className="w-4 h-4 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
                                    <path fillRule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clipRule="evenodd" />
                                </svg>
                                <span>No credit card required</span>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    )
}
