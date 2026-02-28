import type { ColumnDef } from '@tanstack/vue-table'
import type { SalesRecord } from '~/api/datasets'

function formatCurrency(value: number | null | undefined) {
  if (value == null)
    return '—'
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value)
}

function formatDate(value: string | null | undefined) {
  if (!value)
    return '—'
  return new Date(value).toLocaleDateString()
}

export const columns: ColumnDef<SalesRecord>[] = [
  {
    accessorKey: 'order_number',
    header: 'Order #',
  },
  {
    accessorKey: 'order_date',
    header: 'Date',
    cell: ({ getValue }) => formatDate(getValue() as string),
  },
  {
    accessorKey: 'product_line',
    header: 'Product Line',
  },
  {
    accessorKey: 'product_code',
    header: 'Product',
  },
  {
    accessorKey: 'customer_name',
    header: 'Customer',
  },
  {
    accessorKey: 'country',
    header: 'Country',
  },
  {
    accessorKey: 'status',
    header: 'Status',
  },
  {
    accessorKey: 'quantity_ordered',
    header: 'Qty',
  },
  {
    accessorKey: 'price_each',
    header: 'Price',
    cell: ({ getValue }) => formatCurrency(getValue() as number),
  },
  {
    accessorKey: 'total_sales',
    header: 'Total',
    cell: ({ getValue }) => formatCurrency(getValue() as number),
  },
  {
    accessorKey: 'deal_size',
    header: 'Deal Size',
  },
]
