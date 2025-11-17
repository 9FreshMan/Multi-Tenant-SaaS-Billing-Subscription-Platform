import { useAuth } from '../contexts/AuthContext'
import RevenueChart from '../components/RevenueChart'

export default function Dashboard() {
    const { user } = useAuth()

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <h1 className="text-3xl font-bold text-slate-100 tracking-tight">Dashboard</h1>
                <div className="px-4 py-2 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg text-white text-sm font-medium shadow-lg shadow-blue-500/20">
                    Live
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="card group hover:border-blue-500/50 transition-all duration-300">
                    <h3 className="text-sm font-medium text-slate-300 uppercase tracking-wide">Active Subscription</h3>
                    <p className="mt-3 text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">Pro Plan</p>
                    <div className="mt-2 h-1 w-12 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full group-hover:w-full transition-all duration-300"></div>
                </div>

                <div className="card group hover:border-green-500/50 transition-all duration-300">
                    <h3 className="text-sm font-medium text-slate-300 uppercase tracking-wide">Monthly Cost</h3>
                    <p className="mt-3 text-3xl font-bold text-slate-100">$29<span className="text-lg text-slate-300">/mo</span></p>
                    <div className="mt-2 h-1 w-12 bg-gradient-to-r from-green-500 to-emerald-500 rounded-full group-hover:w-full transition-all duration-300"></div>
                </div>

                <div className="card group hover:border-cyan-500/50 transition-all duration-300">
                    <h3 className="text-sm font-medium text-slate-300 uppercase tracking-wide">API Calls</h3>
                    <p className="mt-3 text-3xl font-bold text-slate-100">1,234</p>
                    <p className="text-sm text-slate-300 mt-1">of <span className="text-cyan-400">10,000</span> limit</p>
                    <div className="mt-2 h-1 bg-slate-700 rounded-full overflow-hidden">
                        <div className="h-full w-[12%] bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full"></div>
                    </div>
                </div>

                <div className="card group hover:border-violet-500/50 transition-all duration-300">
                    <h3 className="text-sm font-medium text-slate-300 uppercase tracking-wide">Storage Used</h3>
                    <p className="mt-3 text-3xl font-bold text-slate-100">2.4 GB</p>
                    <p className="text-sm text-slate-300 mt-1">of <span className="text-violet-400">10 GB</span> limit</p>
                    <div className="mt-2 h-1 bg-slate-700 rounded-full overflow-hidden">
                        <div className="h-full w-[24%] bg-gradient-to-r from-violet-500 to-purple-500 rounded-full"></div>
                    </div>
                </div>
            </div>

            {/* Revenue Chart */}
            <div className="card">
                <RevenueChart type="area" height={350} />
            </div>

            <div className="card border-l-4 border-blue-500">
                <div className="flex items-start gap-4">
                    <div className="flex-shrink-0 w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-500 rounded-lg flex items-center justify-center shadow-lg shadow-blue-500/30">
                        <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                        </svg>
                    </div>
                    <div>
                        <h2 className="text-xl font-bold text-slate-100 mb-2">Welcome back, {user?.first_name}!</h2>
                        <p className="text-slate-300 leading-relaxed">
                            Your subscription is active and all systems operational.
                            Monitor usage metrics and manage billing from the navigation menu.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    )
}
