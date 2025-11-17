import { useState, useEffect } from 'react'
import { useToast } from '../components/Toast'
import api from '../services/api'

interface Invoice {
    id: string
    number: string
    date: string
    amount: number
    status: string
}

export default function Invoices() {
    const { showToast, ToastContainer } = useToast()
    const [invoices, setInvoices] = useState<Invoice[]>([])
    const [isLoading, setIsLoading] = useState(true)

    // Load invoices from API
    useEffect(() => {
        const loadInvoices = async () => {
            try {
                const response = await api.get('/invoices')
                const invoicesData = response.data.map((inv: any) => ({
                    id: inv.id,
                    number: inv.invoice_number,
                    date: new Date(inv.invoice_date).toISOString().split('T')[0],
                    amount: parseFloat(inv.total),
                    status: inv.status
                }))
                setInvoices(invoicesData)
            } catch (error) {
                console.error('Failed to load invoices:', error)
                showToast('Failed to load invoices', 'error')
            } finally {
                setIsLoading(false)
            }
        }

        loadInvoices()
    }, [])

    const handleDownload = async (invoice: typeof invoices[0]) => {
        try {
            showToast('Downloading invoice PDF...', 'info')

            // Call backend API to get PDF
            const response = await api.get(`/invoices/${invoice.id}/pdf`, {
                responseType: 'blob'
            })

            // Create blob and download
            const blob = new Blob([response.data], { type: 'application/pdf' })
            const url = window.URL.createObjectURL(blob)
            const a = document.createElement('a')
            a.href = url
            a.download = `${invoice.number}.pdf`
            document.body.appendChild(a)
            a.click()
            document.body.removeChild(a)
            window.URL.revokeObjectURL(url)

            showToast(`Invoice ${invoice.number} downloaded successfully!`, 'success')
        } catch (error) {
            console.error('PDF download error:', error)
            showToast('Failed to download invoice. Please try again.', 'error')
        }
    }

    const handleView = async (invoice: typeof invoices[0]) => {
        try {
            showToast('Opening invoice...', 'info')

            // Call backend API to get PDF
            const response = await api.get(`/invoices/${invoice.id}/pdf`, {
                responseType: 'blob'
            })

            // Create blob and open in new tab
            const blob = new Blob([response.data], { type: 'application/pdf' })
            const url = window.URL.createObjectURL(blob)
            window.open(url, '_blank')

            // Cleanup after a short delay
            setTimeout(() => {
                window.URL.revokeObjectURL(url)
                showToast('Invoice opened successfully', 'success')
            }, 1000)

        } catch (error) {
            console.error('PDF view error:', error)
            showToast('Failed to view invoice. Please try again.', 'error')
        }
    }


    if (isLoading) {
        return (
            <div className="space-y-6">
                <div className="animate-pulse">
                    <div className="h-10 bg-slate-800 rounded-lg w-1/4 mb-6"></div>
                    <div className="card">
                        <div className="space-y-4">
                            <div className="h-4 bg-slate-700 rounded"></div>
                            <div className="h-4 bg-slate-700 rounded w-5/6"></div>
                            <div className="h-4 bg-slate-700 rounded w-4/6"></div>
                        </div>
                    </div>
                </div>
            </div>
        )
    }

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <h1 className="text-3xl font-bold text-slate-100 tracking-tight">Invoices</h1>
                <div className="px-4 py-2 bg-slate-800 rounded-lg border border-slate-700">
                    <span className="text-sm text-slate-400">Total: </span>
                    <span className="text-lg font-bold text-slate-100">{invoices.length}</span>
                </div>
            </div>

            <div className="card overflow-hidden">
                <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-slate-800">
                        <thead className="bg-slate-800/50">
                            <tr>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-slate-300 uppercase tracking-wider">
                                    Invoice Number
                                </th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-slate-300 uppercase tracking-wider">
                                    Date
                                </th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-slate-300 uppercase tracking-wider">
                                    Amount
                                </th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-slate-300 uppercase tracking-wider">
                                    Status
                                </th>
                                <th className="px-6 py-4 text-right text-xs font-semibold text-slate-300 uppercase tracking-wider">
                                    Actions
                                </th>
                            </tr>
                        </thead>
                        <tbody className="bg-slate-900/30 divide-y divide-slate-800">
                            {invoices.map((invoice) => (
                                <tr key={invoice.id} className="hover:bg-slate-800/30 transition-colors">
                                    <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-blue-400">
                                        {invoice.number}
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-400">
                                        {invoice.date}
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-slate-100">
                                        ${invoice.amount.toFixed(2)}
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-green-500/20 text-green-400 border border-green-500/30">
                                            {invoice.status}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-3">
                                        <button
                                            className="text-blue-400 hover:text-blue-300 font-medium transition-colors"
                                            onClick={() => handleDownload(invoice)}
                                        >
                                            Download
                                        </button>
                                        <button
                                            className="text-purple-400 hover:text-purple-300 font-medium transition-colors"
                                            onClick={() => handleView(invoice)}
                                        >
                                            View
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>

            <ToastContainer />
        </div>
    )
}
