<script setup lang="ts">
import { useMeQuery } from '~/api/auth'

const auth = useAuthStore()
const { data: user } = useMeQuery()

watch(user, (u) => {
  if (u) {
    auth.user = u
  }
}, { immediate: true })
</script>

<template>
  <SidebarProvider>
    <AppSidebar />
    <SidebarInset>
      <SiteHeader title="Dashboard" />
      <div class="p-4 flex flex-1 flex-col gap-4">
        <RouterView />
      </div>
    </SidebarInset>
  </SidebarProvider>
</template>
