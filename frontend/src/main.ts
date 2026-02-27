import { createHead } from '@unhead/vue/client'
import { createPinia } from 'pinia'
import { createApp } from 'vue'

import App from './App.vue'
import { router } from './router'

import 'virtual:uno.css'
import './styles/main.css'

const app = createApp(App)

app.use(router)
app.use(createPinia())
app.use(createHead())

app.mount('#app')
