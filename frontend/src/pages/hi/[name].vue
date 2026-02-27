<script setup lang="ts">
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
      <div i-carbon-pedestrian inline-block />
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

    <div>
      <button
        m="3 t6" text-sm btn
        @click="router.back()"
      >
        Back
      </button>
    </div>
  </div>
</template>
