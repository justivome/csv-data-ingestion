<script setup lang="ts">
defineOptions({ name: 'IndexPage' })

useHead({ title: 'Dashboard' })

const auth = useAuthStore()
</script>

<template>
  <div class="flex flex-1 flex-col gap-4 items-center justify-center">
    <div class="text-center">
      <h2 class="text-2xl tracking-tight font-bold">
        Welcome{{ auth.user?.name ? `, ${auth.user.name}` : '' }}
      </h2>
      <p class="text-muted-foreground">
        Your CSV data pipeline dashboard
      </p>
    </div>
  </div>
</template>

<route lang="yaml">
meta:
  layout: dashboard
</route>
