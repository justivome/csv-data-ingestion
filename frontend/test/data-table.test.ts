import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it } from 'vitest'
import DataTable from '../src/components/datasets/DataTable.vue'

const mockRecords = [
  {
    id: 1,
    dataset_id: 1,
    order_number: 10107,
    quantity_ordered: 30,
    price_each: 95.7,
    order_line_number: 2,
    sales: 2871,
    order_date: '2003-02-24T00:00:00',
    status: 'Shipped',
    qtr_id: 1,
    month_id: 2,
    year_id: 2003,
    product_line: 'Motorcycles',
    msrp: 95,
    product_code: 'S10_1678',
    customer_name: 'Land of Toys Inc.',
    city: 'NYC',
    state: 'NY',
    country: 'USA',
    territory: 'NA',
    deal_size: 'Small',
    total_sales: 2871,
  },
]

const stubs = {
  Card: { template: '<div><slot /></div>' },
  CardHeader: { template: '<div><slot /></div>' },
  CardTitle: { template: '<div><slot /></div>' },
  CardContent: { template: '<div><slot /></div>' },
  Table: { template: '<table><slot /></table>' },
  TableHeader: { template: '<thead><slot /></thead>' },
  TableBody: { template: '<tbody><slot /></tbody>' },
  TableRow: { template: '<tr><slot /></tr>' },
  TableHead: { template: '<th @click="$attrs.onClick?.()"><slot /></th>' },
  TableCell: { template: '<td><slot /></td>' },
  Button: { template: '<button :disabled="$attrs.disabled" @click="$attrs.onClick?.()"><slot /></button>' },
  Icon: { template: '<span />' },
}

describe('dataTable', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('renders rows from data prop', () => {
    const wrapper = mount(DataTable, {
      props: {
        records: mockRecords,
        total: 1,
        page: 1,
        pageSize: 15,
        sortBy: 'id',
        sortOrder: 'asc' as const,
      },
      global: { stubs },
    })
    expect(wrapper.findAll('td').length).toBeGreaterThan(0)
    expect(wrapper.text()).toContain('10107')
    expect(wrapper.text()).toContain('Motorcycles')
  })

  it('renders pagination controls', () => {
    const wrapper = mount(DataTable, {
      props: {
        records: mockRecords,
        total: 50,
        page: 1,
        pageSize: 15,
        sortBy: 'id',
        sortOrder: 'asc' as const,
      },
      global: { stubs },
    })
    expect(wrapper.text()).toContain('Page 1 of 4')
    expect(wrapper.text()).toContain('Previous')
    expect(wrapper.text()).toContain('Next')
  })
})
