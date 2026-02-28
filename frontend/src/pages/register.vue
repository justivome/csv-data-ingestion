<script setup lang="ts">
import { useRegisterMutation } from '~/api/auth'

defineOptions({ name: 'RegisterPage' })

useHead({ title: 'Register' })

const auth = useAuthStore()
const router = useRouter()

const form = reactive({ name: '', email: '', password: '' })
const error = ref('')

const { mutateAsync: register, isLoading } = useRegisterMutation()

async function onSubmit() {
  error.value = ''
  try {
    const data = await register(toRaw(form))
    auth.setToken(data.access_token)
    router.push('/')
  }
  catch (err) {
    error.value = (err as any)?.data?.detail || 'Registration failed'
  }
}
</script>

<template>
  <Card>
    <CardHeader class="text-center">
      <CardTitle class="text-xl">
        Create an account
      </CardTitle>
      <CardDescription>
        Enter your details to get started
      </CardDescription>
    </CardHeader>
    <CardContent>
      <form @submit.prevent="onSubmit">
        <div class="gap-6 grid">
          <div v-if="error" class="text-sm text-destructive text-center">
            {{ error }}
          </div>
          <div class="gap-2 grid">
            <Label for="name">Name</Label>
            <Input
              id="name"
              v-model="form.name"
              type="text"
              placeholder="John Doe"
              required
            />
          </div>
          <div class="gap-2 grid">
            <Label for="email">Email</Label>
            <Input
              id="email"
              v-model="form.email"
              type="email"
              placeholder="m@example.com"
              required
            />
          </div>
          <div class="gap-2 grid">
            <Label for="password">Password</Label>
            <Input
              id="password"
              v-model="form.password"
              type="password"
              required
            />
          </div>
          <Button type="submit" class="w-full" :disabled="isLoading">
            Create account
          </Button>
        </div>
        <div class="text-sm mt-4 text-center">
          Already have an account?
          <RouterLink to="/login" class="underline underline-offset-4">
            Login
          </RouterLink>
        </div>
      </form>
    </CardContent>
  </Card>
</template>

<route lang="yaml">
meta:
  layout: auth
</route>
