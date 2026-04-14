<template>
  <section class="quick-section reveal" data-reveal>
    <SectionHeader
      eyebrow="Fast Access"
      title="快捷功能入口"
      description="把常用操作压缩成轻量宫格，让项目、学习、示例和部署入口在一个视觉系统里快速直达。"
    />

    <div class="entry-grid">
      <router-link v-for="item in items" :key="item.id" :to="item.href" class="entry-card">
        <div class="entry-icon">
          <component :is="item.icon" />
        </div>
        <h3>{{ item.title }}</h3>
        <p>{{ item.description }}</p>
      </router-link>
    </div>
  </section>
</template>

<script setup lang="ts">
import SectionHeader from './SectionHeader.vue'
import type { QuickActionItem } from './types'

defineProps<{
  items: QuickActionItem[]
}>()
</script>

<style scoped lang="scss">
@use '@/styles/mixins' as *;

.quick-section {
  display: grid;
  gap: 18px;
}

.entry-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
}

.entry-card {
  @include section-shell;
  padding: 22px 20px;
  display: grid;
  gap: 14px;
  text-align: center;
  transition:
    transform var(--transition-base),
    border-color var(--transition-base),
    box-shadow var(--transition-base);

  &:hover {
    transform: translateY(-2px);
    border-color: var(--line-strong);
    box-shadow: var(--glow-primary);

    .entry-icon {
      color: #ffffff;
      background: linear-gradient(135deg, rgba(59, 130, 246, 0.95), rgba(139, 92, 246, 0.92));
      transform: rotate(6deg) translateY(-1px);
    }
  }

  h3 {
    margin: 0;
    color: var(--text-primary);
    font-size: 17px;
  }

  p {
    margin: 0;
    color: var(--text-secondary);
    line-height: 1.6;
    font-size: 13px;
  }
}

.entry-icon {
  width: 52px;
  height: 52px;
  margin: 0 auto;
  border-radius: 16px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.9), rgba(6, 182, 212, 0.82));
  border: 1px solid rgba(191, 219, 254, 0.26);
  box-shadow: 0 12px 24px rgba(59, 130, 246, 0.2);
  transition:
    transform var(--transition-fast),
    background var(--transition-fast),
    color var(--transition-fast);
}

[data-theme='light'] .entry-icon {
  background: linear-gradient(135deg, rgba(29, 78, 216, 0.94), rgba(8, 145, 178, 0.88));
  border-color: rgba(59, 130, 246, 0.16);
}

@media (max-width: 1080px) {
  .entry-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .entry-grid {
    grid-template-columns: 1fr;
  }
}
</style>
