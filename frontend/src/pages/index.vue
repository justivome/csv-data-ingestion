<script setup lang="ts">
import type { DatasetRead } from '~/api/datasets'
import { useDatasetsQuery } from '~/api/datasets'

defineOptions({ name: 'IndexPage' })
useHead({ title: 'Dashboard' })

const auth = useAuthStore()
const router = useRouter()
const { data } = useDatasetsQuery()

const datasets = computed<DatasetRead[]>(() => data.value?.datasets ?? [])

// Aggregate stats across all datasets
const totalDatasets = computed(() => datasets.value.length)
const totalRows = computed(() => datasets.value.reduce((s, d) => s + d.row_count, 0))
const totalRowsDropped = computed(() => datasets.value.reduce((s, d) => s + d.rows_dropped, 0))
const totalSales = computed(() => datasets.value.reduce((s, d) => s + d.total_sales, 0))
const latestUpload = computed(() => datasets.value[0] ?? null)

const dropRate = computed(() => {
  const total = totalRows.value + totalRowsDropped.value
  return total ? ((totalRowsDropped.value / total) * 100).toFixed(1) : '0.0'
})

function formatCurrency(v: number) {
  if (v >= 1_000_000)
    return `$${(v / 1_000_000).toFixed(2)}M`
  if (v >= 1_000)
    return `$${(v / 1_000).toFixed(1)}k`
  return `$${v.toFixed(2)}`
}

function formatDate(s: string | null | undefined) {
  if (!s)
    return '—'
  return new Date(s).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })
}

const statCards = computed(() => [
  {
    label: 'Datasets',
    value: totalDatasets.value,
    icon: 'i-lucide:database',
    sub: totalDatasets.value === 1 ? '1 file uploaded' : `${totalDatasets.value} files uploaded`,
  },
  {
    label: 'Total Rows',
    value: totalRows.value.toLocaleString(),
    icon: 'i-lucide:rows-3',
    sub: `${dropRate.value}% dropped`,
  },
  {
    label: 'Total Sales',
    value: formatCurrency(totalSales.value),
    icon: 'i-lucide:circle-dollar-sign',
    sub: latestUpload.value ? `Last: ${formatDate(latestUpload.value.uploaded_at)}` : 'No data yet',
  },
  {
    label: 'Rows Dropped',
    value: totalRowsDropped.value.toLocaleString(),
    icon: 'i-lucide:trash-2',
    sub: 'Deduped or invalid',
  },
])
</script>

<template>
  <div class="flex flex-col gap-6">
    <!-- Welcome -->
    <div>
      <h2 class="text-2xl tracking-tight font-bold">
        Welcome back{{ auth.user?.name ? `, ${auth.user.name}` : '' }}
      </h2>
      <p class="text-sm text-muted-foreground">
        Here's an overview of your CSV pipeline activity.
      </p>
    </div>

    <!-- Stat cards -->
    <div class="gap-4 grid grid-cols-2 lg:grid-cols-4">
      <Card v-for="card in statCards" :key="card.label">
        <CardHeader class="pb-2 flex flex-row items-center justify-between">
          <CardTitle class="text-sm text-muted-foreground font-medium">
            {{ card.label }}
          </CardTitle>
          <Icon :name="card.icon" class="text-muted-foreground size-4" />
        </CardHeader>
        <CardContent>
          <p class="text-2xl font-bold">
            {{ card.value }}
          </p>
          <p class="text-xs text-muted-foreground mt-1">
            {{ card.sub }}
          </p>
        </CardContent>
      </Card>
    </div>

    <!-- Content row -->
    <div class="gap-4 grid grid-cols-1 lg:grid-cols-3">
      <!-- Recent datasets -->
      <Card class="lg:col-span-2">
        <CardHeader class="flex flex-row items-center justify-between">
          <CardTitle class="text-base">
            Recent Datasets
          </CardTitle>
          <Button variant="ghost" size="sm" @click="router.push('/datasets')">
            View all
          </Button>
        </CardHeader>
        <CardContent>
          <div v-if="datasets.length" class="divide-y">
            <div
              v-for="ds in datasets.slice(0, 5)"
              :key="ds.id"
              class="py-3 flex cursor-pointer transition-colors items-center justify-between hover:text-foreground/80"
              @click="router.push(`/datasets/${ds.id}`)"
            >
              <div class="flex gap-3 min-w-0 items-center">
                <div class="rounded-md bg-primary/10 flex shrink-0 size-8 items-center justify-center">
                  <Icon name="i-lucide:file-spreadsheet" class="text-primary size-4" />
                </div>
                <div class="min-w-0">
                  <p class="text-sm font-medium truncate">
                    {{ ds.filename }}
                  </p>
                  <p class="text-xs text-muted-foreground">
                    {{ ds.row_count.toLocaleString() }} rows · {{ formatDate(ds.uploaded_at) }}
                  </p>
                </div>
              </div>
              <div class="ml-4 text-right shrink-0">
                <p class="text-sm font-semibold">
                  {{ formatCurrency(ds.total_sales) }}
                </p>
                <p class="text-xs text-muted-foreground">
                  total sales
                </p>
              </div>
            </div>
          </div>
          <div v-else class="text-sm text-muted-foreground py-10 text-center">
            No datasets yet.
            <RouterLink to="/datasets" class="ml-1 underline">
              Upload your first CSV
            </RouterLink>
          </div>
        </CardContent>
      </Card>

      <!-- Quick stats sidebar -->
      <Card>
        <CardHeader>
          <CardTitle class="text-base">
            Pipeline Health
          </CardTitle>
        </CardHeader>
        <CardContent class="flex flex-col gap-4">
          <div class="flex flex-col gap-3">
            <div class="text-sm flex items-center justify-between">
              <span class="text-muted-foreground">Data quality</span>
              <span class="font-medium">{{ (100 - Number(dropRate)).toFixed(1) }}%</span>
            </div>
            <div class="rounded-full bg-muted h-2 overflow-hidden">
              <div
                class="rounded-full bg-primary h-full transition-all"
                :style="{ width: `${100 - Number(dropRate)}%` }"
              />
            </div>
          </div>

          <div class="pt-2 border-t flex flex-col gap-3">
            <div
              v-for="ds in datasets.slice(0, 4)"
              :key="ds.id"
              class="flex gap-3 items-center"
            >
              <div class="flex-1 min-w-0">
                <div class="text-xs mb-1 flex items-center justify-between">
                  <span class="text-muted-foreground truncate">{{ ds.filename.replace('.csv', '') }}</span>
                  <span class="font-medium ml-2 shrink-0">{{ formatCurrency(ds.total_sales) }}</span>
                </div>
                <div class="rounded-full bg-muted h-1.5 overflow-hidden">
                  <div
                    class="rounded-full bg-primary/70 h-full transition-all"
                    :style="{ width: totalSales ? `${(ds.total_sales / totalSales) * 100}%` : '0%' }"
                  />
                </div>
              </div>
            </div>
            <p v-if="!datasets.length" class="text-xs text-muted-foreground py-2 text-center">
              No data yet
            </p>
          </div>

          <div v-if="latestUpload" class="text-xs text-muted-foreground pt-2 border-t space-y-1">
            <div class="flex justify-between">
              <span>Latest upload</span>
              <span class="text-foreground font-medium">{{ formatDate(latestUpload.uploaded_at) }}</span>
            </div>
            <div class="flex justify-between">
              <span>Date range</span>
              <span class="text-foreground font-medium">
                {{ formatDate(latestUpload.date_min) }} – {{ formatDate(latestUpload.date_max) }}
              </span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  </div>
</template>

<route lang="yaml">
meta:
  layout: dashboard
  title: Dashboard
</route>
