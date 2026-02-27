<script setup lang="ts">
import { Button } from '~/components/ui/button'
</script>

<template>
  <nav flex="~ gap-2" mt-6 justify-center>
    <Button as-child variant="ghost" size="icon">
      <RouterLink to="/" title="Home">
        <Icon name="i-lucide:house" />
      </RouterLink>
    </Button>

    <Button variant="ghost" size="icon" title="Toggle dark mode" @click="toggleDark()">
      <Icon name="i-lucide:sun" class="dark:hidden" />
      <Icon name="i-lucide:moon" class="hidden dark:block" />
    </Button>

    <Button as-child variant="ghost" size="icon">
      <RouterLink to="/about" title="About" data-test-id="about">
        <Icon name="i-lucide:info" />
      </RouterLink>
    </Button>

    <Button as-child variant="ghost" size="icon">
      <a rel="noreferrer" href="https://github.com/antfu/vitesse" target="_blank" title="GitHub">
        <Icon name="i-lucide:github" />
      </a>
    </Button>
  </nav>
</template>
