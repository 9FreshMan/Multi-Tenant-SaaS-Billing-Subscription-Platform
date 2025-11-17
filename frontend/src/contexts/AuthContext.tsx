import React, { createContext, useContext, useState, useEffect } from 'react'
import { authService, User } from '../services/auth'

interface AuthContextType {
    user: User | null
    login: (email: string, password: string) => Promise<void>
    logout: () => void
    isLoading: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [user, setUser] = useState<User | null>(null)
    const [isLoading, setIsLoading] = useState(true)

    useEffect(() => {
        const initAuth = async () => {
            const token = localStorage.getItem('access_token')
            if (token) {
                try {
                    const currentUser = await authService.getCurrentUser()
                    setUser(currentUser)
                } catch (error) {
                    localStorage.removeItem('access_token')
                    localStorage.removeItem('refresh_token')
                }
            }
            setIsLoading(false)
        }

        initAuth()
    }, [])

    const login = async (email: string, password: string) => {
        const response = await authService.login({ email, password })
        localStorage.setItem('access_token', response.access_token)
        localStorage.setItem('refresh_token', response.refresh_token)

        const currentUser = await authService.getCurrentUser()
        setUser(currentUser)
    }

    const logout = () => {
        authService.logout()
        setUser(null)
    }

    return (
        <AuthContext.Provider value={{ user, login, logout, isLoading }}>
            {children}
        </AuthContext.Provider>
    )
}

export const useAuth = () => {
    const context = useContext(AuthContext)
    if (!context) {
        throw new Error('useAuth must be used within AuthProvider')
    }
    return context
}
