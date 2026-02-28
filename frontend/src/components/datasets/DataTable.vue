<script setup lang="ts">
import type { DatasetQueryParams, SalesRecord } from '~/api/datasets'
import { FlexRender, getCoreRowModel, useVueTable } from '@tanstack/vue-table'
import { computed } from 'vue'
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationFirst,
  PaginationItem,
  PaginationLast,
  PaginationNext,
  PaginationPrevious,
} from '~/components/ui/pagination'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '~/components/ui/select'
import { columns } from './columns'

const props = defineProps<{
  records: SalesRecord[]
  total: number
  page: number
  pageSize: number
  sortBy: string
  sortOrder: 'asc' | 'desc'
}>()

const emit = defineEmits<{
  sort: [sortBy: string, sortOrder: 'asc' | 'desc']
  filter: [filters: Partial<DatasetQueryParams>]
  pageChange: [page: number]
  pageSizeChange: [pageSize: number]
}>()

const statusFilter = ref('')
const productLineFilter = ref('')

const table = useVueTable({
  get data() { return props.records },
  columns,
  getCoreRowModel: getCoreRowModel(),
  manualPagination: true,
  manualSorting: true,
})

const totalPages = computed(() => Math.ceil(props.total / props.pageSize))
const rangeStart = computed(() => (props.page - 1) * props.pageSize + 1)
const rangeEnd = computed(() => Math.min(props.page * props.pageSize, props.total))

function handleSort(columnId: string) {
  if (props.sortBy === columnId)
    emit('sort', columnId, props.sortOrder === 'asc' ? 'desc' : 'asc')
  else
    emit('sort', columnId, 'asc')
}

// Reka Select can't use empty string as value, so we use '__all__' as sentinel
const ALL = '__all__'

function onStatusChange(value: string) {
  statusFilter.value = value === ALL ? '' : value
  applyFilters()
}

function onProductLineChange(value: string) {
  productLineFilter.value = value === ALL ? '' : value
  applyFilters()
}

function onPageSizeChange(value: string) {
  emit('pageSizeChange', Number(value))
}

function applyFilters() {
  const filters: Partial<DatasetQueryParams> = {}
  if (statusFilter.value)
    filters.status = statusFilter.value
  if (productLineFilter.value)
    filters.product_line = productLineFilter.value
  emit('filter', filters)
}

const statuses = ['Shipped', 'Resolved', 'Cancelled', 'On Hold', 'Disputed', 'In Process']
const productLines = ['Motorcycles', 'Classic Cars', 'Trucks and Buses', 'Vintage Cars', 'Planes', 'Ships', 'Trains']
const pageSizes = [10, 20, 50]
</script>

<template>
  <Card>
    <CardHeader>
      <div class="flex flex-wrap gap-3 items-center justify-between">
        <CardTitle class="text-base">
          Records
        </CardTitle>
        <!-- Per-page selector -->
        <div class="text-sm text-muted-foreground flex gap-2 items-center">
          <span class="shrink-0">Rows per page</span>
          <Select :model-value="String(pageSize)" @update:model-value="onPageSizeChange">
            <SelectTrigger class="w-[75px]">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem v-for="n in pageSizes" :key="n" :value="String(n)">
                {{ n }}
              </SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>
      <!-- Filters -->
      <div class="mt-3 flex flex-wrap gap-3">
        <Select :model-value="statusFilter || ALL" @update:model-value="onStatusChange">
          <SelectTrigger class="w-[160px]">
            <SelectValue placeholder="All Statuses" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem :value="ALL">
              All Statuses
            </SelectItem>
            <SelectItem v-for="s in statuses" :key="s" :value="s">
              {{ s }}
            </SelectItem>
          </SelectContent>
        </Select>
        <Select :model-value="productLineFilter || ALL" @update:model-value="onProductLineChange">
          <SelectTrigger class="w-[190px]">
            <SelectValue placeholder="All Product Lines" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem :value="ALL">
              All Product Lines
            </SelectItem>
            <SelectItem v-for="p in productLines" :key="p" :value="p">
              {{ p }}
            </SelectItem>
          </SelectContent>
        </Select>
      </div>
    </CardHeader>

    <CardContent>
      <div class="border rounded-md overflow-auto">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead
                v-for="header in table.getFlatHeaders()"
                :key="header.id"
                class="cursor-pointer select-none whitespace-nowrap"
                @click="handleSort(header.column.id)"
              >
                <div class="flex gap-1 items-center">
                  <FlexRender :render="header.column.columnDef.header" :props="header.getContext()" />
                  <Icon v-if="sortBy === header.column.id && sortOrder === 'asc'" name="i-lucide:chevron-up" class="size-3.5" />
                  <Icon v-else-if="sortBy === header.column.id && sortOrder === 'desc'" name="i-lucide:chevron-down" class="size-3.5" />
                  <Icon v-else name="i-lucide:chevrons-up-down" class="opacity-30 size-3.5" />
                </div>
              </TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow v-if="!records.length">
              <TableCell :colspan="columns.length" class="text-muted-foreground text-center h-24">
                No records found
              </TableCell>
            </TableRow>
            <TableRow v-for="row in table.getRowModel().rows" :key="row.id">
              <TableCell v-for="cell in row.getVisibleCells()" :key="cell.id" class="whitespace-nowrap">
                <FlexRender :render="cell.column.columnDef.cell" :props="cell.getContext()" />
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </div>

      <!-- Pagination -->
      <div class="mt-4 flex flex-wrap gap-3 items-center justify-between">
        <p class="text-sm text-muted-foreground shrink-0">
          {{ rangeStart }}-{{ rangeEnd }} of {{ total }}
        </p>

        <Pagination
          class="mx-0 w-auto"
          :total="total"
          :items-per-page="pageSize"
          :sibling-count="1"
          show-edges
          :page="page"
          @update:page="emit('pageChange', $event)"
        >
          <PaginationContent v-slot="{ items }">
            <!-- Mobile: just prev / counter / next -->
            <div class="flex gap-1 items-center sm:hidden">
              <PaginationFirst />
              <PaginationPrevious />
              <span class="text-sm px-2">{{ page }} / {{ totalPages }}</span>
              <PaginationNext />
              <PaginationLast />
            </div>

            <!-- Desktop: full pagination -->
            <div class="gap-1 hidden items-center sm:flex">
              <PaginationPrevious />
              <template v-for="(item, index) in items" :key="index">
                <PaginationItem
                  v-if="item.type === 'page'"
                  :value="item.value"
                  :is-active="item.value === page"
                >
                  {{ item.value }}
                </PaginationItem>
                <PaginationEllipsis v-else />
              </template>
              <PaginationNext />
            </div>
          </PaginationContent>
        </Pagination>
      </div>
    </CardContent>
  </Card>
</template>
