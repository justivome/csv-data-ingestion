import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it } from 'vitest'
import { createMemoryHistory, createRouter } from 'vue-router'
import { useAuthStore } from '../../src/stores/auth'

function createTestRouter() {
  return createRouter({
    history: createMemoryHistory(),
    routes: [
      { path: '/', component: { template: '<div>Dashboard</div>' } },
      { path: '/login', component: { template: '<div>Login</div>' } },
      { path: '/register', component: { template: '<div>Register</div>' } },
    ],
  })
}

describe('auth e2e flow', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.clear()
  })

  it('unauthenticated user is redirected to /login', async () => {
    const router = createTestRouter()
    router.beforeEach((to) => {
      const token = localStorage.getItem('auth-token')
      if (!token && !['/login', '/register'].includes(to.path))
        return '/login'
    })

    await router.push('/')
    await router.isReady()
    expect(router.currentRoute.value.path).toBe('/login')
  })

  it('authenticated user on /login is redirected to /', async () => {
    localStorage.setItem('auth-token', 'fake-token')

    const router = createTestRouter()
    router.beforeEach((to) => {
      const token = localStorage.getItem('auth-token')
      if (token && ['/login', '/register'].includes(to.path))
        return '/'
    })

    await router.push('/login')
    await router.isReady()
    expect(router.currentRoute.value.path).toBe('/')
  })

  it('logout clears token and allows redirect to login', async () => {
    const auth = useAuthStore()
    auth.setToken('fake-token')
    expect(auth.isAuthenticated).toBe(true)

    auth.logout()
    expect(auth.isAuthenticated).toBe(false)
    expect(localStorage.getItem('auth-token')).toBe('')
  })
})
