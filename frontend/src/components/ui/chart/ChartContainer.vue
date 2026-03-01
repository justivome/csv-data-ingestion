<script setup lang="ts">
import type { HTMLAttributes } from 'vue'
import type { ChartConfig } from '.'
import { useId } from 'reka-ui'
import { computed, ref } from 'vue'
import { cn } from '~/lib/utils'
import { provideChartContext } from '.'
import ChartStyle from './ChartStyle.vue'

const props = withDefaults(defineProps<{
  id?: HTMLAttributes['id']
  config: ChartConfig
  class?: HTMLAttributes['class']
  cursor?: boolean
}>(), {
  cursor: true,
})

const PREFIX = 'chart'
const generatedId = useId()
const chartId = computed(() => `${PREFIX}-${props.id || generatedId}`)
const configRef = ref(props.config)

provideChartContext({ id: chartId.value, config: configRef })
</script>

<template>
  <div
    :data-chart="chartId"
    :class="cn('flex aspect-video justify-center text-xs [&_.unovis-xy-container]:w-full', props.class)"
    :style="{
      '--vis-tooltip-padding': '8px 12px',
      '--vis-tooltip-background-color': 'hsl(var(--popover))',
      '--vis-tooltip-border-color': 'hsl(var(--border))',
      '--vis-tooltip-text-color': 'hsl(var(--popover-foreground))',
      '--vis-crosshair-line-stroke-color': cursor ? 'hsl(var(--border))' : 'transparent',
    } as any"
  >
    <ChartStyle :id="chartId" />
    <slot :id="chartId" :config="config" />
  </div>
</template>
