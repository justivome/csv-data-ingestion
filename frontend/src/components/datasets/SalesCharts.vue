<script setup lang="ts">
import type { Aggregates } from '~/api/datasets'
import type { ChartConfig } from '~/components/ui/chart'
import { VisAxis, VisGroupedBar, VisLine, VisXYContainer } from '@unovis/vue'
import { computed } from 'vue'
import { ChartContainer, ChartLegendContent } from '~/components/ui/chart'

const props = defineProps<{
  aggregates: Aggregates
}>()

// Sales by Product Line
const productLineConfig: ChartConfig = {
  total_sales: { label: 'Sales', color: 'hsl(var(--primary))' },
}

const productLineData = computed(() =>
  Object.entries(props.aggregates.sales_by_product_line).map(([name, value]) => ({
    name,
    total_sales: value,
  })),
)

// Sales by Country (top 10)
const countryConfig: ChartConfig = {
  total_sales: { label: 'Sales', color: 'hsl(var(--primary))' },
}

const countryData = computed(() =>
  Object.entries(props.aggregates.sales_by_country)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .map(([name, value]) => ({
      name,
      total_sales: value,
    })),
)

// Monthly sales
const monthlyConfig: ChartConfig = {
  total: { label: 'Monthly Sales', color: 'hsl(var(--primary))' },
}

const monthlyData = computed(() =>
  props.aggregates.sales_by_month.map(item => ({
    month: item.month,
    total: item.total,
  })),
)
</script>

<template>
  <div class="gap-4 grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3">
    <!-- Sales by Product Line -->
    <Card>
      <CardHeader>
        <CardTitle class="text-base">
          Sales by Product Line
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ChartContainer :config="productLineConfig" class="flex-col w-full aspect-auto">
          <VisXYContainer :data="productLineData" :height="220" :padding="{ bottom: 20 }">
            <VisGroupedBar :x="(_: any, i: number) => i" :y="[(d: any) => d.total_sales]" :color="() => 'var(--color-total_sales)'" :rounded-corners="4" :bar-padding="0.3" />
            <VisAxis type="x" :tick-format="(i: number) => productLineData[i]?.name ?? ''" :grid-line="false" :tick-line="false" />
            <VisAxis type="y" :tick-format="(v: number) => `$${(v / 1000).toFixed(0)}k`" :grid-line="true" :tick-line="false" :domain-line="false" />
          </VisXYContainer>
          <ChartLegendContent vertical-align="bottom" />
        </ChartContainer>
      </CardContent>
    </Card>

    <!-- Sales by Country (top 10) -->
    <Card>
      <CardHeader>
        <CardTitle class="text-base">
          Sales by Country (Top 10)
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ChartContainer :config="countryConfig" class="flex-col w-full aspect-auto">
          <VisXYContainer :data="countryData" :height="220" :padding="{ bottom: 20 }">
            <VisGroupedBar :x="(_: any, i: number) => i" :y="[(d: any) => d.total_sales]" :color="() => 'var(--color-total_sales)'" :rounded-corners="4" :bar-padding="0.3" />
            <VisAxis type="x" :tick-format="(i: number) => countryData[i]?.name ?? ''" :grid-line="false" :tick-line="false" />
            <VisAxis type="y" :tick-format="(v: number) => `$${(v / 1000).toFixed(0)}k`" :grid-line="true" :tick-line="false" :domain-line="false" />
          </VisXYContainer>
          <ChartLegendContent vertical-align="bottom" />
        </ChartContainer>
      </CardContent>
    </Card>

    <!-- Monthly Sales Over Time -->
    <Card class="md:col-span-2 xl:col-span-1">
      <CardHeader>
        <CardTitle class="text-base">
          Monthly Sales
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ChartContainer :config="monthlyConfig" class="flex-col w-full aspect-auto">
          <VisXYContainer :data="monthlyData" :height="220" :padding="{ bottom: 20 }">
            <VisLine :x="(_: any, i: number) => i" :y="(d: any) => d.total" color="var(--color-total)" />
            <VisAxis type="x" :tick-format="(i: number) => monthlyData[i]?.month ?? ''" :num-ticks="6" :grid-line="false" :tick-line="false" />
            <VisAxis type="y" :tick-format="(v: number) => `$${(v / 1000).toFixed(0)}k`" :grid-line="true" :tick-line="false" :domain-line="false" />
          </VisXYContainer>
          <ChartLegendContent vertical-align="bottom" />
        </ChartContainer>
      </CardContent>
    </Card>
  </div>
</template>
