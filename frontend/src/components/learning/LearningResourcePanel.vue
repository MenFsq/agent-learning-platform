<template>
  <section id="learning-resources" class="resource-panel">
    <SectionHeader
      eyebrow="学习资料"
      title="资料与延伸阅读"
      :description="featuredDescription"
    />

    <div v-if="featuredResources.length" class="featured-block">
      <p class="featured-title">当前节点优先看这些</p>
      <div class="resource-grid">
        <a
          v-for="resource in featuredResources"
          :key="resource.id"
          class="resource-card featured"
          :href="resource.url"
          target="_blank"
          rel="noreferrer"
        >
          <div class="resource-top">
            <span class="resource-type">{{ formatType(resource.type) }}</span>
            <span class="arrow">查看</span>
          </div>
          <h3>{{ resource.title }}</h3>
          <p>{{ resource.description }}</p>
        </a>
      </div>
    </div>

    <div class="resource-grid">
      <a
        v-for="resource in resources"
        :key="resource.id"
        class="resource-card"
        :href="resource.url"
        target="_blank"
        rel="noreferrer"
      >
        <div class="resource-top">
          <span class="resource-type">{{ formatType(resource.type) }}</span>
          <span class="arrow">查看</span>
        </div>
        <h3>{{ resource.title }}</h3>
        <p>{{ resource.description }}</p>
      </a>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'

import SectionHeader from '@/components/dashboard/SectionHeader.vue'
import type { LearningResource } from '@/data/learning/langchainCurriculum'

const props = defineProps<{
  resources: LearningResource[]
  featuredResources: LearningResource[]
  selectedNodeTitle: string
}>()

const formatType = (type: LearningResource['type']) => {
  const labels: Record<LearningResource['type'], string> = {
    guide: '指南',
    docs: '文档',
    practice: '实践',
    community: '社区'
  }

  return labels[type]
}

const featuredDescription = computed(() =>
  props.featuredResources.length
    ? `围绕 ${props.selectedNodeTitle} 优先补最相关的资料，同时保留整张路线图的核心参考入口。`
    : '整合官方文档、练习仓库和社区入口，避免学习时资料散落。'
)
</script>

<style scoped lang="scss">
@use '@/styles/mixins' as *;

.resource-panel {
  @include section-shell;
  padding: 24px;
  display: grid;
  gap: 24px;
}

.featured-block {
  display: grid;
  gap: 14px;
}

.featured-title {
  margin: 0;
  color: var(--text-secondary);
}

.resource-grid {
  display: grid;
  gap: 14px;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
}

.resource-card {
  @include panel-hover;
  display: grid;
  gap: 12px;
  padding: 18px;
  border-radius: var(--radius-lg);
  border: 1px solid var(--line-soft);
  background: rgba(255, 255, 255, 0.04);

  &.featured {
    background: rgba(59, 130, 246, 0.09);
    border-color: rgba(59, 130, 246, 0.2);
  }

  h3 {
    margin: 0;
    font-size: 18px;
  }

  p {
    margin: 0;
    color: var(--text-secondary);
    line-height: 1.65;
  }
}

.resource-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.resource-type {
  color: var(--color-secondary);
  font-size: 12px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

.arrow {
  color: var(--text-muted);
  font-size: 13px;
}
</style>
