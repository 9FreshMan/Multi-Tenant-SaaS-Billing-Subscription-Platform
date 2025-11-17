import UsageChart, { ResourceBreakdownChart } from '../components/UsageChart'

export default function Usage() {
    return (
        <div>
            <h1 className="text-2xl font-bold text-slate-100 mb-6">Usage & Analytics</h1>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                <div className="card">
                    <h3 className="text-sm font-medium text-slate-300">API Calls</h3>
                    <p className="mt-2 text-3xl font-semibold text-slate-100">1,234</p>
                    <p className="text-xs text-slate-300 mt-1">of 10,000 (12.3%)</p>
                    <div className="mt-2 w-full bg-slate-700 rounded-full h-2">
                        <div className="bg-blue-500 h-2 rounded-full" style={{ width: '12.3%' }}></div>
                    </div>
                </div>

                <div className="card">
                    <h3 className="text-sm font-medium text-slate-300">Storage</h3>
                    <p className="mt-2 text-3xl font-semibold text-slate-100">2.4 GB</p>
                    <p className="text-xs text-slate-300 mt-1">of 10 GB (24%)</p>
                    <div className="mt-2 w-full bg-slate-700 rounded-full h-2">
                        <div className="bg-blue-500 h-2 rounded-full" style={{ width: '24%' }}></div>
                    </div>
                </div>

                <div className="card">
                    <h3 className="text-sm font-medium text-slate-300">Bandwidth</h3>
                    <p className="mt-2 text-3xl font-semibold text-slate-100">15 GB</p>
                    <p className="text-xs text-slate-300 mt-1">this month</p>
                </div>

                <div className="card">
                    <h3 className="text-sm font-medium text-slate-300">Active Users</h3>
                    <p className="mt-2 text-3xl font-semibold text-slate-100">3</p>
                    <p className="text-xs text-slate-300 mt-1">of 25</p>
                </div>
            </div>

            {/* Usage Charts */}
            <div className="mb-6">
                <UsageChart metric="all" />
            </div>

            {/* Resource Breakdown */}
            <div className="mb-6">
                <ResourceBreakdownChart />
            </div>

            <div className="card">
                <h2 className="text-lg font-semibold text-slate-100 mb-4">Usage Details</h2>
                <div className="space-y-4">
                    <div className="flex justify-between items-center py-3 border-b border-slate-700">
                        <div>
                            <p className="font-medium text-slate-200">API Calls</p>
                            <p className="text-sm text-slate-300">Daily average: 41 calls</p>
                        </div>
                        <span className="text-sm font-medium text-slate-100">1,234 / 10,000</span>
                    </div>
                    <div className="flex justify-between items-center py-3 border-b border-slate-700">
                        <div>
                            <p className="font-medium text-slate-200">Storage</p>
                            <p className="text-sm text-slate-300">2,456 MB used</p>
                        </div>
                        <span className="text-sm font-medium text-slate-100">2.4 GB / 10 GB</span>
                    </div>
                    <div className="flex justify-between items-center py-3">
                        <div>
                            <p className="font-medium text-slate-200">Bandwidth</p>
                            <p className="text-sm text-slate-300">Transferred this month</p>
                        </div>
                        <span className="text-sm font-medium text-slate-100">15 GB</span>
                    </div>
                </div>
            </div>
        </div>
    )
}
