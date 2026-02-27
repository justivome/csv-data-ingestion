<script setup lang="ts">
import { Button } from '~/components/ui/button'

const props = defineProps<{
  initial: number
}>()

const { count, inc, dec } = useCounter(props.initial)
</script>

<template>
  <div flex="~ items-center gap-2">
    <Button variant="outline" size="icon" @click="dec()">
      <Icon name="i-lucide:minus" />
    </Button>
    <span>{{ count }}</span>
    <Button variant="outline" size="icon" @click="inc()">
      <Icon name="i-lucide:plus" />
    </Button>
  </div>
</template>
