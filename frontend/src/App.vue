<template>
  <div id="app" class="app-shell" :class="{ 'with-header': showHeader }">
    <AppHeader v-if="showHeader" />

    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import AppHeader from './components/Layout/AppHeader.vue'
import { useAppStore } from './store/app'

const route = useRoute()
const appStore = useAppStore()

const showHeader = computed(() => !['Login', 'NotFound'].includes(String(route.name ?? '')))

onMounted(() => {
  appStore.initialize()
})
</script>

<style scoped lang="scss">
.app-shell {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  position: relative;
  z-index: 1;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  transition: padding-top var(--transition-base);
}

.app-shell.with-header .main-content {
  padding-top: var(--header-height);
}
</style>