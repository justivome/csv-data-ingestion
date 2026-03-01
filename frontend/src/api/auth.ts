import { useMutation, useQuery } from '@pinia/colada'
import { useAuthStore } from '~/stores/auth'
import { api } from './client'

interface TokenResponse {
  access_token: string
  token_type: string
}

interface UserResponse {
  id: number
  name: string
  email: string
}

export function useLoginMutation() {
  return useMutation({
    mutation: (data: { email: string, password: string }) =>
      api<TokenResponse>('/login', { method: 'POST', body: data }),
  })
}

export function useRegisterMutation() {
  return useMutation({
    mutation: (data: { name: string, email: string, password: string }) =>
      api<TokenResponse>('/register', { method: 'POST', body: data }),
  })
}

export function useMeQuery() {
  const auth = useAuthStore()
  return useQuery({
    key: ['me'],
    query: () => api<UserResponse>('/me'),
    enabled: () => auth.isAuthenticated,
  })
}
