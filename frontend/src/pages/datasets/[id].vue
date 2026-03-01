<script setup lang="ts">
import type { DatasetQueryParams } from '~/api/datasets'
import { exportDataset, useDatasetDetailQuery } from '~/api/datasets'
import DataTable from '~/components/datasets/DataTable.vue'
import SalesCharts from '~/components/datasets/SalesCharts.vue'

defineOptions({ name: 'DatasetDetailPage' })
useHead({ title: 'Dataset Detail' })

const route = useRoute()
const datasetId = computed(() => Number(route.params.id))

const queryParams = ref<DatasetQueryParams>({
  page: 1,
  page_size: 20,
  sort_by: 'id',
  sort_order: 'asc',
})

const { data } = useDatasetDetailQuery(datasetId, queryParams)

function formatDate(dateStr: string | null | undefined) {
  if (!dateStr)
    return '—'
  return new Date(dateStr).toLocaleDateString()
}

function formatCurrency(value: number | undefined) {
  if (value == null)
    return '—'
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value)
}

function onSort(sortBy: string, sortOrder: 'asc' | 'desc') {
  queryParams.value = { ...queryParams.value, sort_by: sortBy, sort_order: sortOrder, page: 1 }
}

function onFilter(filters: Partial<DatasetQueryParams>) {
  queryParams.value = { ...queryParams.value, ...filters, page: 1 }
}

function onPageChange(page: number) {
  queryParams.value = { ...queryParams.value, page }
}

function onPageSizeChange(pageSize: number) {
  queryParams.value = { ...queryParams.value, page_size: pageSize, page: 1 }
}
</script>

<template>
  <div v-if="data" class="flex flex-col gap-6">
    <!-- Header -->
    <div class="flex items-start justify-between">
      <div>
        <h2 class="text-2xl tracking-tight font-bold">
          {{ data.dataset.filename }}
        </h2>
        <p class="text-sm text-muted-foreground">
          {{ data.dataset.row_count.toLocaleString() }} rows
          · {{ formatCurrency(data.dataset.total_sales) }} total sales
          · {{ formatDate(data.dataset.date_min) }} — {{ formatDate(data.dataset.date_max) }}
        </p>
      </div>
      <div class="flex gap-2">
        <Button variant="outline" size="sm" @click="exportDataset(datasetId, 'csv')">
          <Icon name="i-lucide:download" class="mr-1" />
          CSV
        </Button>
        <Button variant="outline" size="sm" @click="exportDataset(datasetId, 'parquet')">
          <Icon name="i-lucide:download" class="mr-1" />
          Parquet
        </Button>
      </div>
    </div>

    <!-- Charts -->
    <SalesCharts :aggregates="data.aggregates" />

    <!-- Data Table -->
    <DataTable
      :records="data.records"
      :total="data.total"
      :page="data.page"
      :page-size="data.page_size"
      :sort-by="queryParams.sort_by || 'id'"
      :sort-order="queryParams.sort_order || 'asc'"
      @sort="onSort"
      @filter="onFilter"
      @page-change="onPageChange"
      @page-size-change="onPageSizeChange"
    />
  </div>
  <div v-else class="py-12 flex items-center justify-center">
    <Icon name="i-lucide:loader-2" class="mr-2 size-5 animate-spin" />
    Loading...
  </div>
</template>

<route lang="yaml">
meta:
  layout: dashboard
  title: Dataset Detail
</route>
