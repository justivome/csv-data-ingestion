import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it } from 'vitest'
import { useAuthStore } from '../src/stores/auth'

describe('auth store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.clear()
  })

  it('isAuthenticated is false when no token', () => {
    const auth = useAuthStore()
    expect(auth.isAuthenticated).toBe(false)
  })

  it('setToken makes isAuthenticated true', () => {
    const auth = useAuthStore()
    auth.setToken('test-token')
    expect(auth.isAuthenticated).toBe(true)
    expect(auth.token).toBe('test-token')
  })

  it('setToken stores token in state', () => {
    const auth = useAuthStore()
    auth.setToken('persisted-token')
    expect(auth.token).toBe('persisted-token')
  })

  it('logout clears token and user', () => {
    const auth = useAuthStore()
    auth.setToken('test-token')
    auth.user = { id: 1, name: 'Test', email: 'test@example.com' }

    auth.logout()

    expect(auth.isAuthenticated).toBe(false)
    expect(auth.token).toBe('')
    expect(auth.user).toBeNull()
  })
})
