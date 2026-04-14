<template>
  <section class="stage-panel">
    <SectionHeader
      eyebrow="阶段路线"
      title="阶段路线与关键产出"
      description="把知识节点放回阶段视角里看，能更清楚知道每一段学习应该产出什么。"
    />

    <div class="stage-list">
      <article
        v-for="stage in stages"
        :key="stage.id"
        class="stage-card"
        :class="{ active: stage.id === selectedStageId }"
      >
        <div class="card-head">
          <div>
            <p class="stage-order">第 {{ stage.order }} 阶段</p>
            <h3>{{ stage.label }}</h3>
          </div>
          <span class="metric-mono">{{ stage.duration }}</span>
        </div>

        <p class="goal">{{ stage.goal }}</p>

        <div class="stage-highlight">
          <strong>阶段里程碑</strong>
          <p>{{ stage.milestone }}</p>
        </div>

        <div class="focus-row">
          <button
            v-for="nodeId in stage.focusNodeIds"
            :key="nodeId"
            type="button"
            class="focus-chip"
            :class="{ current: nodeId === currentNodeId }"
            @click="$emit('select-node', nodeId)"
          >
            {{ nodeLookup.get(nodeId)?.shortTitle ?? nodeId }}
          </button>
        </div>
      </article>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'

import SectionHeader from '@/components/dashboard/SectionHeader.vue'
import type { LearningNode, LearningStage } from '@/data/learning/langchainCurriculum'

const props = defineProps<{
  stages: LearningStage[]
  nodes: LearningNode[]
  selectedStageId: string
  currentNodeId: string
}>()

defineEmits<{
  (event: 'select-node', nodeId: string): void
}>()

const nodeLookup = computed(() => new Map(props.nodes.map(node => [node.id, node] as const)))
</script>

<style scoped lang="scss">
@use '@/styles/mixins' as *;

.stage-panel {
  @include section-shell;
  padding: 24px;
  display: grid;
  gap: 20px;
}

.stage-list {
  display: grid;
  gap: 16px;
}

.stage-card {
  @include panel-hover;
  border-radius: var(--radius-lg);
  border: 1px solid var(--line-soft);
  background: rgba(255, 255, 255, 0.04);
  padding: 18px;
  display: grid;
  gap: 16px;

  &.active {
    border-color: rgba(59, 130, 246, 0.34);
    box-shadow: var(--glow-primary);
    background: rgba(59, 130, 246, 0.08);
  }
}

.card-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;

  h3 {
    margin: 6px 0 0;
    font-size: 20px;
  }
}

.stage-order {
  margin: 0;
  color: var(--color-secondary);
  font-size: 11px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}

.goal {
  margin: 0;
  color: var(--text-secondary);
  line-height: 1.7;
}

.stage-highlight {
  padding: 14px 16px;
  border-radius: var(--radius-md);
  background: rgba(139, 92, 246, 0.08);
  border: 1px solid rgba(139, 92, 246, 0.18);

  strong {
    display: block;
    margin-bottom: 8px;
  }

  p {
    margin: 0;
    color: var(--text-secondary);
    line-height: 1.65;
  }
}

.focus-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.focus-chip {
  border: 1px solid var(--line-strong);
  background: rgba(255, 255, 255, 0.02);
  color: var(--text-primary);
  border-radius: 999px;
  padding: 8px 12px;
  cursor: pointer;
  transition:
    transform var(--transition-fast),
    border-color var(--transition-fast),
    background var(--transition-fast);

  &:hover {
    transform: translateY(-1px);
    border-color: rgba(6, 182, 212, 0.4);
  }

  &.current {
    background: rgba(34, 197, 94, 0.12);
    border-color: rgba(34, 197, 94, 0.32);
  }
}
</style>
