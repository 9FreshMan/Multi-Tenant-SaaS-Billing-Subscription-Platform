import { useEffect, useState } from 'react'

export type ToastType = 'success' | 'error' | 'warning' | 'info'

interface ToastProps {
    message: string
    type: ToastType
    duration?: number
    onClose: () => void
}

export const Toast: React.FC<ToastProps> = ({ message, type, duration = 5000, onClose }) => {
    useEffect(() => {
        const timer = setTimeout(() => {
            onClose()
        }, duration)

        return () => clearTimeout(timer)
    }, [duration, onClose])

    const icons = {
        success: '✓',
        error: '✕',
        warning: '⚠',
        info: 'ℹ'
    }

    const colors = {
        success: 'bg-green-50 border-green-500 text-green-800',
        error: 'bg-red-50 border-red-500 text-red-800',
        warning: 'bg-yellow-50 border-yellow-500 text-yellow-800',
        info: 'bg-blue-50 border-blue-500 text-blue-800'
    }

    return (
        <div className={`fixed top-4 right-4 max-w-md p-4 rounded-lg border-l-4 shadow-lg z-50 animate-slide-in ${colors[type]}`}>
            <div className="flex items-start">
                <div className="flex-shrink-0 text-xl mr-3">
                    {icons[type]}
                </div>
                <div className="flex-1">
                    <p className="text-sm font-medium">{message}</p>
                </div>
                <button
                    onClick={onClose}
                    className="flex-shrink-0 ml-3 text-gray-400 hover:text-gray-600"
                >
                    ✕
                </button>
            </div>
        </div>
    )
}

// Toast Manager Hook
export const useToast = () => {
    const [toasts, setToasts] = useState<Array<{ id: number; message: string; type: ToastType }>>([])

    const showToast = (message: string, type: ToastType = 'info') => {
        const id = Date.now()
        setToasts(prev => [...prev, { id, message, type }])
    }

    const removeToast = (id: number) => {
        setToasts(prev => prev.filter(toast => toast.id !== id))
    }

    const ToastContainer = () => (
        <>
            {toasts.map(toast => (
                <Toast
                    key={toast.id}
                    message={toast.message}
                    type={toast.type}
                    onClose={() => removeToast(toast.id)}
                />
            ))}
        </>
    )

    return { showToast, ToastContainer }
}
