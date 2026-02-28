// @ts-expect-error - virtual module
import { setupLayouts } from 'virtual:generated-layouts'
import { createRouter, createWebHistory } from 'vue-router'
import { routes } from 'vue-router/auto-routes'

export const router = createRouter({
  history: createWebHistory(),
  routes: setupLayouts(routes),
})

router.beforeEach((to) => {
  const token = localStorage.getItem('auth-token')
  const isAuthenticated = !!token

  const publicPages = ['/login', '/register']
  const isPublicPage = publicPages.includes(to.path)

  if (!isAuthenticated && !isPublicPage) {
    return '/login'
  }

  if (isAuthenticated && isPublicPage) {
    return '/'
  }
})
