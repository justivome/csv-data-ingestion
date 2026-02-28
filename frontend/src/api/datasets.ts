import type { MaybeRefOrGetter } from 'vue'
import { useMutation, useQuery } from '@pinia/colada'
import { computed, toValue } from 'vue'
import { api } from '~/api/client'

export interface DateRange {
  min: string
  max: string
}

export interface UploadResponse {
  dataset_id: number
  row_count: number
  rows_dropped: number
  date_range: DateRange
  total_sales: number
}

export interface DatasetRead {
  id: number
  filename: string
  uploaded_at: string
  row_count: number
  rows_dropped: number
  date_min: string | null
  date_max: string | null
  total_sales: number
}

export interface SalesRecord {
  id: number
  dataset_id: number
  order_number: number
  quantity_ordered: number
  price_each: number
  order_line_number: number
  sales: number
  order_date: string | null
  status: string | null
  qtr_id: number | null
  month_id: number | null
  year_id: number | null
  product_line: string | null
  msrp: number | null
  product_code: string | null
  customer_name: string | null
  city: string | null
  state: string | null
  country: string | null
  territory: string | null
  deal_size: string | null
  total_sales: number
}

export interface SalesByMonth {
  month: string
  total: number
}

export interface Aggregates {
  sales_by_product_line: Record<string, number>
  sales_by_country: Record<string, number>
  sales_by_month: SalesByMonth[]
}

export interface DatasetDetailResponse {
  dataset: DatasetRead
  records: SalesRecord[]
  total: number
  page: number
  page_size: number
  aggregates: Aggregates
}

export interface DatasetQueryParams {
  page?: number
  page_size?: number
  sort_by?: string
  sort_order?: 'asc' | 'desc'
  status?: string
  product_line?: string
  date_from?: string
  date_to?: string
}

export function useUploadMutation() {
  return useMutation({
    mutation: (file: File) => {
      const formData = new FormData()
      formData.append('file', file)
      return api<UploadResponse>('/upload', {
        method: 'POST',
        body: formData,
      })
    },
  })
}

export function useDatasetsQuery() {
  return useQuery({
    key: ['datasets'],
    query: () => api<{ datasets: DatasetRead[] }>('/datasets'),
  })
}

export function useDatasetDetailQuery(
  id: MaybeRefOrGetter<number>,
  params: MaybeRefOrGetter<DatasetQueryParams> = {},
) {
  return useQuery({
    key: computed(() => ['datasets', toValue(id), toValue(params)]),
    placeholderData: (previousData: DatasetDetailResponse | undefined) => previousData,
    query: () => {
      const p = toValue(params)
      const query: Record<string, string> = {}
      if (p.page)
        query.page = String(p.page)
      if (p.page_size)
        query.page_size = String(p.page_size)
      if (p.sort_by)
        query.sort_by = p.sort_by
      if (p.sort_order)
        query.sort_order = p.sort_order
      if (p.status)
        query.status = p.status
      if (p.product_line)
        query.product_line = p.product_line
      if (p.date_from)
        query.date_from = p.date_from
      if (p.date_to)
        query.date_to = p.date_to
      return api<DatasetDetailResponse>(`/datasets/${toValue(id)}`, { query })
    },
  })
}

export function exportDataset(id: number, format: 'csv' | 'parquet') {
  const token = localStorage.getItem('auth-token')
  const url = `/api/datasets/${id}/export?format=${format}`
  const a = document.createElement('a')
  // Use fetch to get blob with auth header
  fetch(url, {
    headers: { Authorization: `Bearer ${token}` },
  })
    .then(r => r.blob())
    .then((blob) => {
      const blobUrl = URL.createObjectURL(blob)
      a.href = blobUrl
      a.download = `export.${format}`
      a.click()
      URL.revokeObjectURL(blobUrl)
    })
}
