<template>
  <section class="ticker reveal" data-reveal>
    <div class="ticker-label">
      <span>Community Feed</span>
    </div>
    <div class="ticker-track">
      <div class="ticker-inner">
        <template v-for="item in duplicatedItems" :key="`${item.id}-${item.title}`">
          <a
            v-if="item.external"
            :href="item.href"
            target="_blank"
            rel="noreferrer noopener"
            class="ticker-item"
          >
            <strong>{{ item.title }}</strong>
            <span>{{ item.detail }}</span>
          </a>
          <router-link
            v-else
            :to="item.href"
            class="ticker-item"
          >
            <strong>{{ item.title }}</strong>
            <span>{{ item.detail }}</span>
          </router-link>
        </template>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'

import type { CommunityTickerItem } from './types'

const props = defineProps<{
  items: CommunityTickerItem[]
}>()

const duplicatedItems = computed(() => [...props.items, ...props.items])
</script>

<style scoped lang="scss">
@use '@/styles/mixins' as *;

.ticker {
  @include section-shell;
  display: grid;
  grid-template-columns: auto minmax(0, 1fr);
  align-items: center;
  gap: 16px;
  padding: 16px 18px;
}

.ticker-label {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 42px;
  padding: 0 16px;
  border-radius: 999px;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.9), rgba(139, 92, 246, 0.82));
  color: #ffffff;
  border: 1px solid rgba(191, 219, 254, 0.26);
  box-shadow: 0 12px 24px rgba(59, 130, 246, 0.18);
  font-size: 12px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}

[data-theme='light'] .ticker-label {
  background: linear-gradient(135deg, rgba(29, 78, 216, 0.94), rgba(124, 58, 237, 0.88));
  border-color: rgba(59, 130, 246, 0.16);
}

.ticker-track {
  overflow: hidden;
}

.ticker-inner {
  display: flex;
  gap: 18px;
  width: max-content;
  animation: ticker-scroll 24s linear infinite;
}

.ticker:hover .ticker-inner {
  animation-play-state: paused;
}

.ticker-item {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  white-space: nowrap;
  color: var(--text-secondary);
  transition: color var(--transition-fast);

  strong {
    color: var(--text-primary);
    font-size: 14px;
  }

  span::before {
    content: '•';
    margin-right: 10px;
    color: var(--color-secondary);
  }

  &:hover {
    color: var(--text-primary);
  }
}

@keyframes ticker-scroll {
  from {
    transform: translateX(0);
  }

  to {
    transform: translateX(-50%);
  }
}

@media (max-width: 768px) {
  .ticker {
    grid-template-columns: 1fr;
  }
}
</style>
