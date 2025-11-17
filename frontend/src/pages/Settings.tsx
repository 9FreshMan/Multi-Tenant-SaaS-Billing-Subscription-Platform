import { useState, useEffect } from 'react'
import { useToast } from '../components/Toast'
import api from '../services/api'

export default function Settings() {
    const [companyName, setCompanyName] = useState('')
    const [email, setEmail] = useState('')
    const [phone, setPhone] = useState('')
    const [billingEmail, setBillingEmail] = useState('')
    const [isSaving, setIsSaving] = useState(false)
    const { showToast, ToastContainer } = useToast()

    // Load tenant data on mount
    useEffect(() => {
        const loadTenantData = async () => {
            try {
                const response = await api.get('/tenants/me')
                const tenant = response.data
                setCompanyName(tenant.name || '')
                setEmail(tenant.email || '')
                setPhone(tenant.phone || '')
                setBillingEmail(tenant.email || '') // Using same email for billing
            } catch (error) {
                console.error('Failed to load tenant data:', error)
                showToast('Failed to load settings', 'error')
            }
        }

        loadTenantData()
    }, [])

    const handleSaveChanges = async () => {
        setIsSaving(true)
        try {
            // Call backend to persist tenant settings
            const payload = {
                name: companyName,
                email,
                phone,
                address_line1: null,
                address_line2: null,
                city: null,
                state: null,
                country: null,
                postal_code: null,
            }

            await api.put('/tenants/me', payload)
            showToast('Settings saved successfully!', 'success')
        } catch (error) {
            console.error('Failed to save settings:', error)
            showToast('Failed to save settings', 'error')
        } finally {
            setIsSaving(false)
        }
    }

    const handleUpdatePaymentMethod = () => {
        showToast('Redirecting to Stripe billing portal...', 'info')
        // In production: window.location.href = stripePortalUrl
    }

    const handleDeleteAccount = async () => {
        // Replace blocking confirm with non-blocking UX: user must click Delete to confirm
        showToast('Account deletion requested — this is a demo; no data will be deleted.', 'warning')
        // In production: await api.delete('/users/me') and then redirect
    }

    return (
        <div>
            <h1 className="text-2xl font-bold text-slate-100 mb-6">Settings</h1>

            <div className="card mb-6">
                <h2 className="text-lg font-semibold text-slate-100 mb-4">Company Information</h2>
                <div className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-slate-200">Company Name</label>
                        <input
                            type="text"
                            className="mt-1 input"
                            value={companyName}
                            onChange={(e) => setCompanyName(e.target.value)}
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-slate-200">Company Slug</label>
                        <input type="text" className="mt-1 input" defaultValue="acme-inc" disabled />
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <label className="block text-sm font-medium text-slate-200">Email</label>
                            <input
                                type="email"
                                className="mt-1 input"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-slate-200">Phone</label>
                            <input
                                type="tel"
                                className="mt-1 input"
                                value={phone}
                                onChange={(e) => setPhone(e.target.value)}
                            />
                        </div>
                    </div>
                    <button
                        className="btn btn-primary"
                        onClick={handleSaveChanges}
                        disabled={isSaving}
                    >
                        {isSaving ? 'Saving...' : 'Save Changes'}
                    </button>
                </div>
            </div>

            <div className="card mb-6">
                <h2 className="text-lg font-semibold text-slate-100 mb-4">Billing Information</h2>
                <div className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-slate-200">Payment Method</label>
                        <div className="mt-2 flex items-center">
                            <div className="flex-1 p-3 border border-slate-600 rounded-lg bg-slate-800/50">
                                <div className="flex items-center">
                                    <svg className="w-8 h-6 mr-2" viewBox="0 0 32 20" fill="none">
                                        <rect width="32" height="20" rx="3" fill="#1434CB" />
                                        <path d="M11.5 7L9.5 13H11L13 7H11.5Z" fill="white" />
                                        <path d="M14 10L15 7H16.5L15.5 10H17L16 13H14.5L15.5 10H14Z" fill="white" />
                                    </svg>
                                    <div>
                                        <p className="font-medium text-slate-100">Visa ending in 4242</p>
                                        <p className="text-sm text-slate-300">Expires 12/2025</p>
                                    </div>
                                </div>
                            </div>
                            <button
                                className="ml-3 btn btn-secondary"
                                onClick={handleUpdatePaymentMethod}
                            >
                                Update
                            </button>
                        </div>
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-slate-200">Billing Email</label>
                        <input
                            type="email"
                            className="mt-1 input"
                            value={billingEmail}
                            onChange={(e) => setBillingEmail(e.target.value)}
                        />
                    </div>
                </div>
            </div>

            <div className="card">
                <h2 className="text-lg font-semibold text-slate-100 mb-4">Danger Zone</h2>
                <div className="border border-red-500/50 rounded-lg p-4 bg-red-500/10">
                    <h3 className="font-medium text-slate-100">Delete Account</h3>
                    <p className="text-sm text-slate-300 mt-1">
                        Once you delete your account, there is no going back. Please be certain.
                    </p>
                    <button
                        className="mt-4 btn btn-danger"
                        onClick={handleDeleteAccount}
                    >
                        Delete Account
                    </button>
                </div>
            </div>

            <ToastContainer />
        </div>
    )
}
