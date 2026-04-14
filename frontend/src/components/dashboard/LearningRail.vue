<template>
  <section class="learning-section reveal" data-reveal>
    <SectionHeader
      eyebrow="Learning Momentum"
      title="我的学习路径"
      description="把当前学习主题与完成进度保持在线，让学习成为工作流的一部分。"
      action-label="继续学习"
      action-href="/learning"
    />

    <div class="rail">
      <article v-for="item in items" :key="item.id" class="learning-card">
        <div class="learning-head">
          <div class="learning-icon">
            <component :is="item.icon" />
          </div>
          <span v-if="item.completed" class="learning-badge">Completed</span>
        </div>

        <div>
          <p class="learning-category">{{ item.category }}</p>
          <h3>{{ item.title }}</h3>
        </div>

        <div class="learning-progress">
          <div class="progress-row">
            <span>{{ item.duration }}</span>
            <span class="metric-mono">{{ item.progress }}%</span>
          </div>
          <div class="progress-bar">
            <span :style="{ width: `${item.progress}%` }"></span>
          </div>
        </div>

        <router-link :to="`/learning`" class="learning-link">继续学习</router-link>
      </article>
    </div>
  </section>
</template>

<script setup lang="ts">
import SectionHeader from './SectionHeader.vue'
import type { LearningItem } from './types'

defineProps<{
  items: LearningItem[]
}>()
</script>

<style scoped lang="scss">
@use '@/styles/mixins' as *;

.learning-section {
  display: grid;
  gap: 18px;
}

.rail {
  @include hidden-scrollbar;
  display: grid;
  grid-auto-flow: column;
  grid-auto-columns: minmax(260px, 320px);
  gap: 16px;
  overflow-x: auto;
  padding-top: 10px;
  padding-bottom: 6px;
  margin-top: -10px;
}

.learning-card {
  @include section-shell;
  @include panel-hover;
  padding: 22px;
  display: grid;
  gap: 18px;
}

.learning-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.learning-icon {
  width: 46px;
  height: 46px;
  border-radius: 16px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.92), rgba(6, 182, 212, 0.84));
  color: #ffffff;
  border: 1px solid rgba(191, 219, 254, 0.28);
  box-shadow: 0 12px 24px rgba(6, 182, 212, 0.2);
}

[data-theme='light'] .learning-icon {
  background: linear-gradient(135deg, rgba(29, 78, 216, 0.94), rgba(8, 145, 178, 0.88));
  border-color: rgba(59, 130, 246, 0.16);
}

.learning-badge {
  padding: 6px 10px;
  border-radius: 999px;
  background: rgba(34, 197, 94, 0.14);
  color: #8ce5a0;
  font-size: 11px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.learning-category {
  margin: 0 0 10px;
  color: var(--color-secondary);
  font-size: 12px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

h3 {
  margin: 0;
  font-size: 22px;
  color: var(--text-primary);
}

.progress-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
  color: var(--text-secondary);
}

.progress-bar {
  height: 8px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.06);
  overflow: hidden;

  span {
    display: block;
    height: 100%;
    border-radius: inherit;
    background: linear-gradient(90deg, var(--color-secondary), var(--color-accent));
  }
}

.learning-link {
  color: var(--text-secondary);
  transition:
    transform var(--transition-fast),
    color var(--transition-fast);

  &:hover {
    color: var(--text-primary);
    transform: translateX(2px);
  }
}
</style>
