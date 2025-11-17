import { useNavigate } from 'react-router-dom'
import { useToast } from '../components/Toast'

export default function Subscriptions() {
    const navigate = useNavigate()
    const { showToast, ToastContainer } = useToast()

    const handleChangePlan = () => {
        navigate('/plans')
        setTimeout(() => {
            showToast('Select a new plan below. Changes will be prorated.', 'info')
        }, 300)
    }

    const handleCancelSubscription = () => {
        showToast('Subscription cancelled. Your Pro Plan will remain active until the end of the billing period.', 'warning')
        // In production: await api.delete('/subscriptions/me')
    }

    return (
        <div>
            <h1 className="text-2xl font-bold text-slate-100 mb-6">Subscriptions</h1>

            <div className="card mb-6">
                <h2 className="text-lg font-semibold text-slate-100 mb-4">Current Subscription</h2>
                <div className="flex items-center justify-between">
                    <div>
                        <p className="text-2xl font-bold text-slate-100">Pro Plan</p>
                        <p className="text-sm text-slate-300">Active since January 15, 2024</p>
                    </div>
                    <div className="text-right">
                        <p className="text-2xl font-bold text-slate-100">$29.00</p>
                        <p className="text-sm text-slate-300">per month</p>
                    </div>
                </div>
                <div className="mt-6 pt-6 border-t border-slate-700">
                    <div className="flex justify-between text-sm">
                        <span className="text-slate-300">Next billing date</span>
                        <span className="font-medium text-slate-100">February 15, 2024</span>
                    </div>
                    <div className="flex justify-between text-sm mt-2">
                        <span className="text-slate-300">Status</span>
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-500/20 text-green-400">
                            Active
                        </span>
                    </div>
                </div>
                <div className="mt-6 flex gap-3">
                    <button
                        className="btn btn-primary"
                        onClick={handleChangePlan}
                    >
                        Change Plan
                    </button>
                    <button
                        className="btn btn-secondary"
                        onClick={handleCancelSubscription}
                    >
                        Cancel Subscription
                    </button>
                </div>
            </div>

            <div className="card">
                <h2 className="text-lg font-semibold text-slate-100 mb-4">Subscription History</h2>
                <div className="space-y-4">
                    <div className="flex items-center justify-between py-3 border-b border-slate-700">
                        <div>
                            <p className="font-medium text-slate-100">Pro Plan</p>
                            <p className="text-sm text-slate-300">Started Jan 15, 2024</p>
                        </div>
                        <span className="text-sm text-green-400">Active</span>
                    </div>
                    <div className="flex items-center justify-between py-3 border-b border-slate-700">
                        <div>
                            <p className="font-medium text-slate-100">Free Plan</p>
                            <p className="text-sm text-slate-300">Dec 1, 2023 - Jan 15, 2024</p>
                        </div>
                        <span className="text-sm text-slate-400">Ended</span>
                    </div>
                </div>
            </div>

            <ToastContainer />
        </div>
    )
}
