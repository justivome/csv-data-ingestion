<script setup lang="ts">
import { Input } from '~/components/ui/input'

const modelValue = defineModel<string>()
</script>

<template>
  <Input
    id="input"
    v-model="modelValue"
    v-bind="$attrs"
    type="text"
    max-w-sm
  />
</template>
