<script setup lang="ts">
import { useMeQuery } from '~/api/auth'

const auth = useAuthStore()
const { data: user } = useMeQuery()

const route = useRoute()

watch(user, (u) => {
  if (u) {
    auth.user = u
  }
}, { immediate: true })
</script>

<template>
  <SidebarProvider class="overflow-hidden h-svh">
    <AppSidebar />
    <main class="flex flex-1 flex-col min-w-0 overflow-y-auto">
      <SiteHeader :title="route.meta.title as string || 'Dashboard'" />
      <div class="p-4 flex flex-1 flex-col gap-4">
        <RouterView />
      </div>
    </main>
  </SidebarProvider>
</template>
