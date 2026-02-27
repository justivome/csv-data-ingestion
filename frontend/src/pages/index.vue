<script setup lang="ts">
import { Button } from '~/components/ui/button'

defineOptions({
  name: 'IndexPage',
})
const user = useUserStore()
const name = ref(user.savedName)

const router = useRouter()
function go() {
  if (name.value)
    router.push(`/hi/${encodeURIComponent(name.value)}`)
}

const { data } = useFetch('/api/health')

useHead({
  title: 'Home',
})
</script>

<template>
  <div>
    <div text-4xl>
      <Icon name="i-lucide:mountain" />
    </div>
    <p>
      <a rel="noreferrer" href="https://github.com/antfu/vitesse" target="_blank">
        Vitesse
      </a>
    </p>
    <p>
      <em text-sm opacity-75>Description</em>
      {{ data }}
    </p>

    <div py-4 />

    <TheInput
      v-model="name"
      placeholder="What's your name?"
      autocomplete="false"
      @keydown.enter="go"
    />
    <label class="hidden" for="input">What's your name?</label>

    <div mt-3>
      <Button class="w-full" :disabled="!name" @click="go">
        Go
      </Button>
    </div>
  </div>
</template>

<route lang="yaml">
meta:
  layout: home
</route>
