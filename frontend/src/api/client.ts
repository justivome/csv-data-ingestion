import { ofetch } from 'ofetch'
import { router } from '~/router'

export const api = ofetch.create({
  baseURL: '/api',
  onRequest({ options }) {
    const token = localStorage.getItem('auth-token')
    if (token) {
      const headers = new Headers(options.headers as HeadersInit)
      headers.set('Authorization', `Bearer ${token}`)
      options.headers = headers
    }
  },
  onResponseError({ response }) {
    if (response.status === 401) {
      localStorage.removeItem('auth-token')
      router.push('/login')
    }
  },
})
