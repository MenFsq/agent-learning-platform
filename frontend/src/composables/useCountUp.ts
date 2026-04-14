import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'

interface CountUpOptions {
  duration?: number
  decimals?: number
  suffix?: string
}

export const useCountUp = (target: number, options: CountUpOptions = {}) => {
  const current = ref(0)
  let frame = 0

  const duration = options.duration ?? 1200
  const decimals = options.decimals ?? 0
  const suffix = options.suffix ?? ''

  const stop = () => {
    if (frame) {
      cancelAnimationFrame(frame)
      frame = 0
    }
  }

  const run = (value: number) => {
    stop()

    const start = performance.now()

    const tick = (now: number) => {
      const progress = Math.min((now - start) / duration, 1)
      const eased = 1 - Math.pow(1 - progress, 3)

      current.value = value * eased

      if (progress < 1) {
        frame = requestAnimationFrame(tick)
      }
    }

    frame = requestAnimationFrame(tick)
  }

  const formatted = computed(() => `${current.value.toFixed(decimals)}${suffix}`)

  onMounted(() => {
    run(target)
  })

  watch(
    () => target,
    value => {
      run(value)
    }
  )

  onBeforeUnmount(() => {
    stop()
  })

  return {
    current,
    formatted
  }
}
