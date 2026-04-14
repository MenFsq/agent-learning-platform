<template>
  <section class="detail-card">
    <div class="detail-hero">
      <div class="meta-row">
        <span class="kind-badge" :class="node.track">{{ node.track === 'roadmap' ? '学习阶段' : '知识节点' }}</span>
        <span class="metric-mono">{{ node.estimatedTime }}</span>
      </div>

      <div>
        <p class="stage-label">{{ stage.label }}</p>
        <h3>{{ node.title }}</h3>
        <p class="summary">{{ node.summary }}</p>
      </div>

      <div class="highlight-box">
        <strong>为什么值得先学</strong>
        <p>{{ node.whyItMatters }}</p>
      </div>
    </div>

    <div class="detail-grid">
      <section class="detail-section">
        <h4>核心要点</h4>
        <ul>
          <li v-for="item in node.keyConcepts" :key="item">{{ item }}</li>
        </ul>
      </section>

      <section class="detail-section">
        <h4>前置知识</h4>
        <div class="chip-row">
          <button
            v-for="item in prerequisiteNodes"
            :key="item.id"
            type="button"
            class="chip"
            @click="$emit('select-node', item.id)"
          >
            {{ item.shortTitle }}
          </button>
          <span v-if="prerequisiteNodes.length === 0" class="empty-tip">无需前置节点，可以直接开始。</span>
        </div>
      </section>

      <section class="detail-section">
        <h4>建议练习</h4>
        <ul>
          <li v-for="task in node.practiceTasks" :key="task">{{ task }}</li>
        </ul>
      </section>

      <section class="detail-section">
        <h4>阶段产出</h4>
        <ul>
          <li v-for="deliverable in node.deliverables" :key="deliverable">{{ deliverable }}</li>
        </ul>
      </section>

      <section class="detail-section">
        <h4>常见坑</h4>
        <ul>
          <li v-for="pitfall in node.pitfalls" :key="pitfall">{{ pitfall }}</li>
        </ul>
      </section>

      <section class="detail-section">
        <h4>通过标准</h4>
        <ul>
          <li v-for="item in node.validation" :key="item">{{ item }}</li>
        </ul>
      </section>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'

import type { LearningNode, LearningStage } from '@/data/learning/langchainCurriculum'

const props = defineProps<{
  node: LearningNode
  stage: LearningStage
  allNodes: LearningNode[]
}>()

defineEmits<{
  (event: 'select-node', nodeId: string): void
}>()

const prerequisiteNodes = computed(() => {
  const lookup = new Map(props.allNodes.map(node => [node.id, node] as const))
  return props.node.prerequisites.map(nodeId => lookup.get(nodeId)).filter((node): node is LearningNode => Boolean(node))
})
</script>

<style scoped lang="scss">
@use '@/styles/mixins' as *;

.detail-card {
  @include section-shell;
  padding: 24px;
  display: grid;
  gap: 24px;
}

.detail-hero {
  display: grid;
  gap: 16px;
}

.meta-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  color: var(--text-secondary);
  font-size: 13px;
}

.kind-badge {
  padding: 8px 12px;
  border-radius: 999px;
  border: 1px solid var(--line-strong);
  font-size: 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;

  &.roadmap {
    background: rgba(59, 130, 246, 0.16);
    color: #8dc3ff;
  }

  &.knowledge {
    background: rgba(139, 92, 246, 0.18);
    color: #d8bbff;
  }
}

.stage-label {
  margin: 0 0 10px;
  color: var(--color-secondary);
  font-size: 12px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}

h3 {
  margin: 0;
  font-size: clamp(24px, 2.4vw, 30px);
}

.summary {
  margin: 12px 0 0;
  color: var(--text-secondary);
  line-height: 1.75;
}

.highlight-box {
  padding: 16px 18px;
  border-radius: var(--radius-lg);
  background: rgba(59, 130, 246, 0.08);
  border: 1px solid rgba(59, 130, 246, 0.16);

  strong {
    display: block;
    margin-bottom: 8px;
  }

  p {
    margin: 0;
    color: var(--text-secondary);
    line-height: 1.7;
  }
}

.detail-grid {
  display: grid;
  gap: 18px;
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.detail-section {
  padding: 18px;
  border-radius: var(--radius-lg);
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--line-soft);

  h4 {
    margin: 0 0 14px;
    font-size: 16px;
  }

  ul {
    margin: 0;
    padding-left: 18px;
    display: grid;
    gap: 10px;
    color: var(--text-secondary);
    line-height: 1.65;
  }
}

.chip-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.chip {
  border: 1px solid var(--line-strong);
  background: rgba(255, 255, 255, 0.04);
  color: var(--text-primary);
  border-radius: 999px;
  padding: 8px 12px;
  cursor: pointer;
  transition:
    transform var(--transition-fast),
    border-color var(--transition-fast),
    color var(--transition-fast);

  &:hover {
    transform: translateY(-1px);
    border-color: rgba(59, 130, 246, 0.4);
    color: var(--color-secondary);
  }
}

.empty-tip {
  color: var(--text-muted);
  line-height: 1.6;
}

@media (max-width: 900px) {
  .detail-grid {
    grid-template-columns: 1fr;
  }
}
</style>
