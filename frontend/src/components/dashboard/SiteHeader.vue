<script setup lang="ts">
defineProps<{
  title?: string
}>()
</script>

<template>
  <header class="px-4 border-b bg-background flex shrink-0 gap-2 h-16 items-center top-0 sticky z-10">
    <SidebarTrigger class="-ml-1" />
    <Separator orientation="vertical" class="mr-2 h-4" />
    <h1 class="text-sm font-medium">
      {{ title }}
    </h1>
  </header>
</template>
