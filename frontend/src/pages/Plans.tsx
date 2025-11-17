import { useState } from 'react'
import { useToast } from '../components/Toast'

export default function Plans() {
    const [selectedPlan, setSelectedPlan] = useState<string | null>(null)
    const [isProcessing, setIsProcessing] = useState(false)
    const { showToast, ToastContainer } = useToast()

    const handleSelectPlan = async (planName: string, _price: number) => {
        setSelectedPlan(planName)
        setIsProcessing(true)

        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1500))

        if (planName === 'Free') {
            // Non-blocking downgrade notice
            showToast(`Downgrade to ${planName} scheduled. You will lose access to advanced features at the end of the billing period.`, 'warning')
        } else if (planName === 'Enterprise') {
            showToast('Sales team will contact you within 24 hours!', 'info')
        } else {
            showToast(`Successfully upgraded to ${planName} Plan! 🎉`, 'success')
        }

        setIsProcessing(false)
        setSelectedPlan(null)
    }

    return (
        <div>
            <h1 className="text-2xl font-bold text-slate-100 mb-6">Subscription Plans</h1>
            <p className="text-slate-300 mb-8">Choose the plan that fits your needs</p>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Free Plan */}
                <div className="card border-2 border-slate-700 hover:border-slate-600 transition-all">
                    <div className="text-center">
                        <h3 className="text-lg font-semibold text-slate-100">Free</h3>
                        <div className="mt-4">
                            <span className="text-4xl font-bold text-slate-100">$0</span>
                            <span className="text-slate-300">/month</span>
                        </div>
                    </div>
                    <ul className="mt-6 space-y-4">
                        <li className="flex items-center text-sm text-slate-300">
                            <span className="mr-2">✓</span> 5 users
                        </li>
                        <li className="flex items-center text-sm text-slate-300">
                            <span className="mr-2">✓</span> 1,000 API calls/month
                        </li>
                        <li className="flex items-center text-sm text-slate-300">
                            <span className="mr-2">✓</span> 5 GB storage
                        </li>
                        <li className="flex items-center text-sm text-slate-300">
                            <span className="mr-2">✓</span> Email support
                        </li>
                    </ul>
                    <button
                        className="mt-6 w-full btn btn-secondary"
                        onClick={() => handleSelectPlan('Free', 0)}
                        disabled={isProcessing}
                    >
                        {selectedPlan === 'Free' && isProcessing ? 'Processing...' : 'Downgrade'}
                    </button>
                </div>

                {/* Pro Plan */}
                <div className="card border-2 border-blue-500 hover:border-blue-400 transition-all shadow-lg">
                    <div className="text-center">
                        <span className="inline-block px-3 py-1 text-xs font-semibold text-blue-400 bg-blue-500/20 rounded-full mb-2">
                            POPULAR
                        </span>
                        <h3 className="text-lg font-semibold text-slate-100">Pro</h3>
                        <div className="mt-4">
                            <span className="text-4xl font-bold text-slate-100">$29</span>
                            <span className="text-slate-300">/month</span>
                        </div>
                    </div>
                    <ul className="mt-6 space-y-4">
                        <li className="flex items-center text-sm text-slate-300">
                            <span className="mr-2">✓</span> 25 users
                        </li>
                        <li className="flex items-center text-sm text-slate-300">
                            <span className="mr-2">✓</span> 10,000 API calls/month
                        </li>
                        <li className="flex items-center text-sm text-slate-300">
                            <span className="mr-2">✓</span> 50 GB storage
                        </li>
                        <li className="flex items-center text-sm text-slate-300">
                            <span className="mr-2">✓</span> Priority support
                        </li>
                        <li className="flex items-center text-sm text-slate-300">
                            <span className="mr-2">✓</span> Advanced analytics
                        </li>
                    </ul>
                    <button
                        className="mt-6 w-full btn btn-primary bg-green-600 hover:bg-green-700"
                        disabled={true}
                    >
                        ✓ Current Plan
                    </button>
                </div>

                {/* Enterprise Plan */}
                <div className="card border-2 border-slate-700 hover:border-slate-600 transition-all">
                    <div className="text-center">
                        <h3 className="text-lg font-semibold text-slate-100">Enterprise</h3>
                        <div className="mt-4">
                            <span className="text-4xl font-bold text-slate-100">$99</span>
                            <span className="text-slate-300">/month</span>
                        </div>
                    </div>
                    <ul className="mt-6 space-y-4">
                        <li className="flex items-center text-sm text-slate-300">
                            <span className="mr-2">✓</span> Unlimited users
                        </li>
                        <li className="flex items-center text-sm text-slate-300">
                            <span className="mr-2">✓</span> Unlimited API calls
                        </li>
                        <li className="flex items-center text-sm text-slate-300">
                            <span className="mr-2">✓</span> 500 GB storage
                        </li>
                        <li className="flex items-center text-sm text-slate-300">
                            <span className="mr-2">✓</span> 24/7 phone support
                        </li>
                        <li className="flex items-center text-sm text-slate-300">
                            <span className="mr-2">✓</span> Custom integrations
                        </li>
                        <li className="flex items-center text-sm text-slate-300">
                            <span className="mr-2">✓</span> Dedicated account manager
                        </li>
                    </ul>
                    <button
                        className="mt-6 w-full btn btn-primary"
                        onClick={() => handleSelectPlan('Enterprise', 99)}
                        disabled={isProcessing}
                    >
                        {selectedPlan === 'Enterprise' && isProcessing ? 'Processing...' : 'Contact Sales'}
                    </button>
                </div>
            </div>

            <ToastContainer />
        </div>
    )
}
