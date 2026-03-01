import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import UploadForm from '../src/components/datasets/UploadForm.vue'

// Mock the API
vi.mock('../src/api/datasets', () => ({
  useUploadMutation: () => ({
    mutate: vi.fn(),
    isLoading: false,
  }),
}))

// Mock router
vi.mock('vue-router', () => ({
  useRouter: () => ({ push: vi.fn() }),
  useRoute: () => ({ params: {} }),
}))

describe('uploadForm', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('renders upload form', () => {
    const wrapper = mount(UploadForm, {
      global: {
        stubs: {
          Card: { template: '<div><slot /></div>' },
          CardHeader: { template: '<div><slot /></div>' },
          CardTitle: { template: '<div><slot /></div>' },
          CardDescription: { template: '<div><slot /></div>' },
          CardContent: { template: '<div><slot /></div>' },
          Input: { template: '<input />' },
          Button: { template: '<button><slot /></button>' },
          Icon: { template: '<span />' },
        },
      },
    })
    expect(wrapper.text()).toContain('Upload CSV')
    expect(wrapper.find('input').exists()).toBe(true)
    expect(wrapper.find('button').exists()).toBe(true)
  })

  it('shows error when no file selected', async () => {
    const wrapper = mount(UploadForm, {
      global: {
        stubs: {
          Card: { template: '<div><slot /></div>' },
          CardHeader: { template: '<div><slot /></div>' },
          CardTitle: { template: '<div><slot /></div>' },
          CardDescription: { template: '<div><slot /></div>' },
          CardContent: { template: '<div><slot /></div>' },
          Input: { template: '<input />' },
          Button: { template: '<button @click="$attrs.onClick?.()"><slot /></button>' },
          Icon: { template: '<span />' },
        },
      },
    })
    await wrapper.find('button').trigger('click')
    expect(wrapper.text()).toContain('Please select a CSV file')
  })
})
