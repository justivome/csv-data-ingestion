<script setup lang="ts">
import { isDark, toggleDark } from '~/composables/dark'

const auth = useAuthStore()
const router = useRouter()

const initials = computed(() => {
  const name = auth.user?.name || ''
  return name
    .split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
})

function logout() {
  auth.logout()
  router.push('/login')
}
</script>

<template>
  <DropdownMenu>
    <DropdownMenuTrigger as-child>
      <SidebarMenuButton size="lg" class="data-[state=open]:bg-sidebar-accent">
        <Avatar class="rounded-lg h-8 w-8" shape="square">
          <AvatarFallback class="rounded-lg">
            {{ initials }}
          </AvatarFallback>
        </Avatar>
        <div class="text-sm leading-tight text-left flex-1 grid">
          <span class="font-semibold truncate">{{ auth.user?.name }}</span>
          <span class="text-xs truncate">{{ auth.user?.email }}</span>
        </div>
        <Icon name="i-lucide:chevrons-up-down" class="ml-auto size-4" />
      </SidebarMenuButton>
    </DropdownMenuTrigger>
    <DropdownMenuContent
      class="rounded-lg min-w-56 w-[--reka-popper-anchor-width]"
      side="bottom"
      align="end"
      :side-offset="4"
    >
      <DropdownMenuLabel class="font-normal p-0">
        <div class="text-sm px-1 py-1.5 text-left flex gap-2 items-center">
          <Avatar class="rounded-lg h-8 w-8" shape="square">
            <AvatarFallback class="rounded-lg">
              {{ initials }}
            </AvatarFallback>
          </Avatar>
          <div class="text-sm leading-tight text-left flex-1 grid">
            <span class="font-semibold truncate">{{ auth.user?.name }}</span>
            <span class="text-xs truncate">{{ auth.user?.email }}</span>
          </div>
        </div>
      </DropdownMenuLabel>
      <DropdownMenuSeparator />
      <DropdownMenuItem @click="toggleDark()">
        <Icon :name="isDark ? 'i-lucide:sun' : 'i-lucide:moon'" />
        {{ isDark ? 'Light mode' : 'Dark mode' }}
      </DropdownMenuItem>
      <DropdownMenuSeparator />
      <DropdownMenuItem @click="logout">
        <Icon name="i-lucide:log-out" />
        Log out
      </DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>
</template>
