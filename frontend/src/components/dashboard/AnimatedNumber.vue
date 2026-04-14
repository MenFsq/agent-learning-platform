<template>
  <span class="metric-mono">{{ formatted }}</span>
</template>

<script setup lang="ts">
import { useCountUp } from '@/composables/useCountUp'

const props = withDefaults(
  defineProps<{
    value: number
    suffix?: string
    duration?: number
    decimals?: number
  }>(),
  {
    suffix: '',
    duration: 1200,
    decimals: 0
  }
)

const { formatted } = useCountUp(props.value, {
  suffix: props.suffix,
  duration: props.duration,
  decimals: props.decimals
})
</script>
