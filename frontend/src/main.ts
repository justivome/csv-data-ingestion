import { PiniaColada } from '@pinia/colada'
import { PiniaColadaAutoRefetch } from '@pinia/colada-plugin-auto-refetch'
import { PiniaColadaRetry } from '@pinia/colada-plugin-retry'
import { createHead } from '@unhead/vue/client'
import { createPinia } from 'pinia'
import { createApp } from 'vue'

import App from './App.vue'
import { router } from './router'

import 'virtual:uno.css'
import './styles/main.css'

const app = createApp(App)

app.use(router)
app.use(createHead())
app.use(createPinia())
app.use(PiniaColada, {
  plugins: [PiniaColadaAutoRefetch(), PiniaColadaRetry()],
})

app.mount('#app')
