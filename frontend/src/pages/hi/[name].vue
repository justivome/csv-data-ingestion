<script setup lang="ts">
import { Button } from '~/components/ui/button'

const router = useRouter()
const route = useRoute('/hi/[name]')
const user = useUserStore()

watchEffect(() => {
  user.setNewName(route.params.name)
})
useHead({
  title: `Hi ${user.savedName}`,
})
</script>

<template>
  <div>
    <div text-4xl>
      <Icon name="i-lucide:user" />
    </div>
    <p>
      Hi {{ user.savedName }}
    </p>

    <p text-sm opacity-75>
      <em>Dynamic route</em>
    </p>

    <template v-if="user.otherNames.length">
      <div text-sm mt-4>
        <span opacity-75>Also known as:</span>
        <ul>
          <li v-for="otherName in user.otherNames" :key="otherName">
            <RouterLink :to="`/hi/${otherName}`" replace>
              {{ otherName }}
            </RouterLink>
          </li>
        </ul>
      </div>
    </template>

    <div mt-6>
      <Button variant="outline" @click="router.back()">
        Back
      </Button>
    </div>
  </div>
</template>
