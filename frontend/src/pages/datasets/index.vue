<script setup lang="ts">
import { useDatasetsQuery } from '~/api/datasets'
import UploadForm from '~/components/datasets/UploadForm.vue'

defineOptions({ name: 'DatasetsPage' })
useHead({ title: 'Datasets' })

const { data, refresh } = useDatasetsQuery()
const router = useRouter()

function formatDate(dateStr: string | null) {
  if (!dateStr)
    return '—'
  return new Date(dateStr).toLocaleDateString()
}

function formatCurrency(value: number) {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value)
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <div>
      <h2 class="text-2xl tracking-tight font-bold">
        Datasets
      </h2>
      <p class="text-muted-foreground">
        Upload and manage your CSV datasets
      </p>
    </div>

    <UploadForm @uploaded="refresh()" />

    <div v-if="data?.datasets?.length" class="gap-4 grid lg:grid-cols-3 md:grid-cols-2">
      <Card
        v-for="ds in data.datasets"
        :key="ds.id"
        class="cursor-pointer transition-shadow hover:shadow-md"
        @click="router.push(`/datasets/${ds.id}`)"
      >
        <CardHeader>
          <CardTitle class="text-base truncate">
            {{ ds.filename }}
          </CardTitle>
          <CardDescription>
            Uploaded {{ formatDate(ds.uploaded_at) }}
          </CardDescription>
        </CardHeader>
        <CardContent class="text-sm gap-2 grid grid-cols-2">
          <div>
            <span class="text-muted-foreground">Rows:</span>
            <span class="font-medium ml-1">{{ ds.row_count.toLocaleString() }}</span>
          </div>
          <div>
            <span class="text-muted-foreground">Dropped:</span>
            <span class="font-medium ml-1">{{ ds.rows_dropped }}</span>
          </div>
          <div class="col-span-2">
            <span class="text-muted-foreground">Total Sales:</span>
            <span class="font-medium ml-1">{{ formatCurrency(ds.total_sales) }}</span>
          </div>
          <div class="text-xs text-muted-foreground col-span-2">
            {{ formatDate(ds.date_min) }} — {{ formatDate(ds.date_max) }}
          </div>
        </CardContent>
      </Card>
    </div>

    <div v-else-if="data" class="text-muted-foreground py-12 text-center">
      No datasets yet. Upload a CSV to get started.
    </div>
  </div>
</template>

<route lang="yaml">
meta:
  layout: dashboard
  title: Datasets
</route>
