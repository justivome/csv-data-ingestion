<script setup lang="ts">
const navItems = [
  { title: 'Dashboard', icon: 'i-lucide:layout-dashboard', to: '/' },
  { title: 'Datasets', icon: 'i-lucide:database', to: '/datasets' },
]
</script>

<template>
  <Sidebar>
    <SidebarHeader>
      <SidebarMenu>
        <SidebarMenuItem>
          <SidebarMenuButton size="lg" as-child>
            <a href="/">
              <div class="text-primary-foreground rounded-lg bg-primary flex size-8 aspect-square items-center justify-center">
                <Icon name="i-lucide:mountain" class="size-4" />
              </div>
              <div class="text-sm leading-tight text-left flex-1 grid">
                <span class="font-semibold truncate">CSV Pipeline</span>
                <span class="text-xs truncate">Data Ingestion</span>
              </div>
            </a>
          </SidebarMenuButton>
        </SidebarMenuItem>
      </SidebarMenu>
    </SidebarHeader>
    <SidebarContent>
      <SidebarGroup>
        <SidebarGroupLabel>Navigation</SidebarGroupLabel>
        <SidebarGroupContent>
          <SidebarMenu>
            <SidebarMenuItem v-for="item in navItems" :key="item.title">
              <SidebarMenuButton as-child>
                <RouterLink :to="item.to">
                  <Icon :name="item.icon" />
                  <span>{{ item.title }}</span>
                </RouterLink>
              </SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroupContent>
      </SidebarGroup>
    </SidebarContent>
    <SidebarFooter>
      <SidebarMenu>
        <SidebarMenuItem>
          <NavUser />
        </SidebarMenuItem>
      </SidebarMenu>
    </SidebarFooter>
  </Sidebar>
</template>
