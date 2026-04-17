<template>
  <div class="app-page-shell" :class="shellClasses">
    <div v-if="$slots.header" class="app-page-header" :class="headerClass">
      <slot name="header" />
    </div>

    <div class="app-page-body" :class="bodyClass">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

type ClassName = string | string[] | Record<string, boolean>

const props = withDefaults(defineProps<{
  mode?: 'page' | 'clip'
  bodyClass?: ClassName
  headerClass?: ClassName
}>(), {
  mode: 'page',
  bodyClass: '',
  headerClass: ''
})

const shellClasses = computed(() => (props.mode === 'page' ? 'app-page-scroll' : 'app-page-clip'))
</script>
