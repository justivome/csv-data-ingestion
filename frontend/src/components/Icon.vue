<script setup lang="ts">
import type { HTMLAttributes } from 'vue'

const props = defineProps<{
  name: string
  class?: HTMLAttributes['class']
}>()
</script>

<template>
  <i
    :class="[name, cn('size-5 inline-block', props.class)]"
  />
</template>
