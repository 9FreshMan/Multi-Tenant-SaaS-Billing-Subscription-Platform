import api from './api'

export interface LoginRequest {
    email: string
    password: string
}

export interface RegisterRequest {
    tenant_name: string
    tenant_slug: string
    email: string
    password: string
    first_name: string
    last_name: string
}

export interface TokenResponse {
    access_token: string
    refresh_token: string
    token_type: string
}

export interface User {
    id: string
    email: string
    first_name: string
    last_name: string
    role: string
    tenant_id: string
}

export const authService = {
    async login(data: LoginRequest): Promise<TokenResponse> {
        const response = await api.post('/auth/login', data)
        return response.data
    },

    async register(data: RegisterRequest): Promise<TokenResponse> {
        const response = await api.post('/auth/register', data)
        return response.data
    },

    async getCurrentUser(): Promise<User> {
        const response = await api.get('/users/me')
        return response.data
    },

    logout() {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
    },
}
