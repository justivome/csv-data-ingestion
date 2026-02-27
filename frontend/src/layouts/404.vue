<script setup lang="ts">
import { Button } from '~/components/ui/button'

const router = useRouter()
useHead({
  title: 'Not Found',
})
</script>

<template>
  <main p="x4 y10" text="center teal-700 dark:gray-200">
    <div text-4xl>
      <Icon name="i-lucide:triangle-alert" />
    </div>
    <RouterView />
    <div>
      <Button variant="outline" class="mt-8" @click="router.back()">
        Back
      </Button>
    </div>
  </main>
</template>
