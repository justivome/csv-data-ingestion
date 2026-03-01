import { useLocalStorage } from '@vueuse/core'
import { defineStore } from 'pinia'

export interface AuthUser {
  id: number
  name: string
  email: string
}

export const useAuthStore = defineStore('auth', () => {
  const token = useLocalStorage('auth-token', '')
  const user = ref<AuthUser | null>(null)

  const isAuthenticated = computed(() => !!token.value)

  function setToken(newToken: string) {
    token.value = newToken
  }

  function logout() {
    token.value = ''
    user.value = null
  }

  return {
    token,
    user,
    isAuthenticated,
    setToken,
    logout,
  }
})
