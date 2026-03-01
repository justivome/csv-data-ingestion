<script setup lang="ts">
import { useLoginMutation } from '~/api/auth'

defineOptions({ name: 'LoginPage' })

useHead({ title: 'Login' })

const auth = useAuthStore()
const router = useRouter()

const form = reactive({ email: '', password: '' })
const error = ref('')

const { mutateAsync: login, isLoading } = useLoginMutation()

async function onSubmit() {
  error.value = ''
  try {
    const data = await login(toRaw(form))
    auth.setToken(data.access_token)
    router.push('/')
  }
  catch (err) {
    error.value = (err as any)?.data?.detail || 'Invalid email or password'
  }
}
</script>

<template>
  <Card>
    <CardHeader class="text-center">
      <CardTitle class="text-xl">
        Welcome back
      </CardTitle>
      <CardDescription>
        Login to your account
      </CardDescription>
    </CardHeader>
    <CardContent>
      <form @submit.prevent="onSubmit">
        <div class="gap-6 grid">
          <div v-if="error" class="text-sm text-destructive text-center">
            {{ error }}
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
            Login
          </Button>
        </div>
        <div class="text-sm mt-4 text-center">
          Don't have an account?
          <RouterLink to="/register" class="underline underline-offset-4">
            Sign up
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
