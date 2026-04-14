<template>
  <section class="overview-block reveal" data-reveal>
    <div class="stats-grid">
      <article v-for="item in items" :key="item.id" class="stat-card">
        <div class="stat-header">
          <div class="stat-icon">
            <component :is="item.icon" />
          </div>
          <span class="stat-delta">{{ item.delta }}</span>
        </div>

        <div class="stat-value">
          <AnimatedNumber :value="item.value" :suffix="item.suffix" />
        </div>
        <p class="stat-label">{{ item.label }}</p>
        <p class="stat-hint">{{ item.hint }}</p>

        <svg viewBox="0 0 100 28" class="sparkline" aria-hidden="true">
          <defs>
            <linearGradient :id="`spark-${item.id}`" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="rgba(59, 130, 246, 0.2)" />
              <stop offset="100%" stop-color="rgba(139, 92, 246, 0.9)" />
            </linearGradient>
          </defs>
          <polyline
            :points="buildPoints(item.sparkline)"
            fill="none"
            :stroke="`url(#spark-${item.id})`"
            stroke-width="3"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
      </article>
    </div>
  </section>
</template>

<script setup lang="ts">
import AnimatedNumber from './AnimatedNumber.vue'
import type { OverviewMetric } from './types'

defineProps<{
  items: OverviewMetric[]
}>()

const buildPoints = (values: number[]) => {
  const max = Math.max(...values)
  const min = Math.min(...values)
  const range = max - min || 1

  return values
    .map((value, index) => {
      const x = (index / Math.max(values.length - 1, 1)) * 100
      const y = 24 - ((value - min) / range) * 18
      return `${x},${y}`
    })
    .join(' ')
}
</script>

<style scoped lang="scss">
@use '@/styles/mixins' as *;

.stats-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 16px;
}

.stat-card {
  @include section-shell;
  @include panel-hover;
  padding: 22px;
}

.stat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.stat-icon {
  width: 42px;
  height: 42px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 14px;
  color: #ffffff;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.92), rgba(6, 182, 212, 0.84));
  border: 1px solid rgba(191, 219, 254, 0.28);
  box-shadow: 0 12px 24px rgba(59, 130, 246, 0.22);
}

[data-theme='light'] .stat-icon {
  background: linear-gradient(135deg, rgba(29, 78, 216, 0.94), rgba(8, 145, 178, 0.88));
  border-color: rgba(59, 130, 246, 0.16);
}

.stat-delta {
  font-size: 12px;
  color: var(--color-secondary);
}

.stat-value {
  margin-top: 20px;
  font-size: clamp(28px, 3vw, 38px);
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1;
}

.stat-label {
  margin: 12px 0 0;
  color: var(--text-primary);
  font-weight: 500;
}

.stat-hint {
  margin: 8px 0 18px;
  color: var(--text-muted);
  line-height: 1.6;
  min-height: 44px;
}

.sparkline {
  width: 100%;
  height: 36px;
  opacity: 0.9;
}

@media (max-width: 1180px) {
  .stats-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 760px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
