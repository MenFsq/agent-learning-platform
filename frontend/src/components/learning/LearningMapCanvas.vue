<template>
  <section id="learning-map" class="map-panel">
    <div class="panel-head">
      <div>
        <p class="eyebrow">交互地图</p>
        <h3>知识地图与阶段路线</h3>
        <p class="panel-copy">点击任意节点，右侧会同步显示更详细的学习信息、练习建议和验证标准。</p>
      </div>

      <div class="toolbar">
        <button type="button" class="toolbar-btn" @click="zoomOutMap">缩小</button>
        <button type="button" class="toolbar-btn" @click="fitMap">适配画布</button>
        <button type="button" class="toolbar-btn" @click="focusSelectedNode">聚焦当前节点</button>
        <button type="button" class="toolbar-btn" @click="zoomInMap">放大</button>
      </div>
    </div>

    <div class="map-surface">
      <VueFlow
        :nodes="flowNodes"
        :edges="flowEdges"
        :min-zoom="0.45"
        :max-zoom="1.7"
        :default-viewport="{ x: 0, y: 0, zoom: 0.75 }"
        :fit-view-on-init="true"
        :apply-default="false"
        :nodes-draggable="false"
        :elements-selectable="true"
        :zoom-on-double-click="false"
        :pan-on-drag="true"
        class="learning-flow"
        @node-click="handleNodeClick"
        @init="handleInit"
      >
        <template #node-learning="nodeProps">
          <div
            class="custom-node"
            :class="[
              `track-${nodeProps.data.track}`,
              {
                selected: nodeProps.data.selected,
                related: nodeProps.data.related
              }
            ]"
          >
            <div class="node-top">
              <span class="node-kind">{{ nodeProps.data.kind === 'stage' ? '阶段' : '主题' }}</span>
              <span class="node-time metric-mono">{{ nodeProps.data.estimatedTime }}</span>
            </div>
            <strong>{{ nodeProps.data.shortTitle }}</strong>
            <p>{{ nodeProps.data.tagline }}</p>
            <div class="node-meta">
              <span>{{ nodeProps.data.stageLabel }}</span>
              <span>{{ nodeProps.data.difficulty }}</span>
            </div>
          </div>
        </template>
      </VueFlow>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, nextTick, watch } from 'vue'
import { Position, VueFlow, useVueFlow, type Edge, type Node } from '@vue-flow/core'
import type { NodeMouseEvent } from '@vue-flow/core'

import type { LearningConnection, LearningNode } from '@/data/learning/langchainCurriculum'

interface FlowNodeData {
  shortTitle: string
  tagline: string
  estimatedTime: string
  difficulty: string
  stageLabel: string
  track: LearningNode['track']
  kind: LearningNode['kind']
  selected: boolean
  related: boolean
}

const props = defineProps<{
  nodes: LearningNode[]
  connections: LearningConnection[]
  selectedNodeId: string
}>()

const emit = defineEmits<{
  (event: 'select-node', nodeId: string): void
}>()

const { fitView, zoomIn, zoomOut, setCenter } = useVueFlow()

const difficultyLabels: Record<LearningNode['difficulty'], string> = {
  Starter: '入门',
  Intermediate: '进阶',
  Advanced: '高级'
}

const nodeLookup = computed(() => new Map(props.nodes.map(node => [node.id, node] as const)))

const selectedNode = computed(() => nodeLookup.value.get(props.selectedNodeId) ?? props.nodes[0])

const selectedStageId = computed(() => selectedNode.value.stageId)

const activeNodeIds = computed(() => {
  const node = selectedNode.value
  const ids = new Set<string>([node.id, ...node.prerequisites, ...node.connectsTo])

  props.nodes.forEach(item => {
    if (item.stageId === selectedStageId.value) {
      ids.add(item.id)
    }
  })

  if (node.kind === 'stage') {
    props.nodes.forEach(item => {
      if (item.stageId === node.id) {
        ids.add(item.id)
      }
    })
  }

  props.connections.forEach(connection => {
    if (connection.source === node.id || connection.target === node.id) {
      ids.add(connection.source)
      ids.add(connection.target)
    }
  })

  return ids
})

const activeEdgeIds = computed(() => {
  const ids = new Set<string>()

  props.connections.forEach(connection => {
    if (
      activeNodeIds.value.has(connection.source) &&
      activeNodeIds.value.has(connection.target) &&
      (connection.source === selectedNode.value.id ||
        connection.target === selectedNode.value.id ||
        connection.source === selectedStageId.value ||
        connection.target === selectedStageId.value)
    ) {
      ids.add(connection.id)
    }
  })

  return ids
})

const flowNodes = computed<Node<FlowNodeData>[]>(() =>
  props.nodes.map(node => ({
    id: node.id,
    type: 'learning',
    position: node.position,
    sourcePosition: Position.Right,
    targetPosition: Position.Left,
    draggable: false,
    connectable: false,
    selectable: true,
    data: {
      shortTitle: node.shortTitle,
      tagline: node.tagline,
      estimatedTime: node.estimatedTime,
      difficulty: difficultyLabels[node.difficulty],
      stageLabel: nodeLookup.value.get(node.stageId)?.shortTitle ?? node.stageId,
      track: node.track,
      kind: node.kind,
      selected: node.id === selectedNode.value.id,
      related: activeNodeIds.value.has(node.id)
    }
  }))
)

const flowEdges = computed<Edge[]>(() =>
  props.connections.map(connection => ({
    id: connection.id,
    source: connection.source,
    target: connection.target,
    type: 'smoothstep',
    animated: activeEdgeIds.value.has(connection.id),
    label: connection.label,
    class: activeEdgeIds.value.has(connection.id) ? 'is-active' : 'is-muted',
    style: {
      stroke: activeEdgeIds.value.has(connection.id)
        ? connection.relation === 'sequence'
          ? '#22c55e'
          : '#3b82f6'
        : 'rgba(148, 163, 184, 0.24)',
      strokeWidth: activeEdgeIds.value.has(connection.id) ? 2.4 : 1.2
    }
  }))
)

const handleInit = async () => {
  await nextTick()
  await fitMap()
}

const handleNodeClick = ({ node }: NodeMouseEvent) => {
  emit('select-node', node.id)
}

const zoomInMap = async () => {
  await zoomIn({ duration: 220 })
}

const zoomOutMap = async () => {
  await zoomOut({ duration: 220 })
}

const fitMap = async () => {
  await fitView({ duration: 260, padding: { x: 80, y: 80 }, maxZoom: 1.15 })
}

const focusSelectedNode = async () => {
  const node = selectedNode.value
  await setCenter(node.position.x + 90, node.position.y + 48, {
    duration: 280,
    zoom: node.kind === 'stage' ? 0.88 : 1
  })
}

watch(
  () => props.selectedNodeId,
  async () => {
    await nextTick()
    await focusSelectedNode()
  }
)

defineExpose({
  fitMap,
  focusSelectedNode
})
</script>

<style scoped lang="scss">
@use '@/styles/mixins' as *;

.map-panel {
  @include section-shell;
  padding: 24px;
  display: grid;
  gap: 20px;
}

.panel-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 18px;
}

.eyebrow {
  margin: 0 0 10px;
  color: var(--color-secondary);
  font-size: 11px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
}

h3 {
  margin: 0;
  font-size: 28px;
}

.panel-copy {
  margin: 12px 0 0;
  color: var(--text-secondary);
  line-height: 1.7;
  max-width: 720px;
}

.toolbar {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.toolbar-btn {
  border: 1px solid var(--line-strong);
  background: rgba(255, 255, 255, 0.04);
  color: var(--text-primary);
  border-radius: 999px;
  padding: 10px 14px;
  cursor: pointer;
  transition:
    transform var(--transition-fast),
    border-color var(--transition-fast),
    background var(--transition-fast);

  &:hover {
    transform: translateY(-1px);
    border-color: rgba(59, 130, 246, 0.38);
    background: rgba(59, 130, 246, 0.12);
  }
}

.map-surface {
  height: 620px;
  border-radius: var(--radius-xl);
  overflow: hidden;
  border: 1px solid var(--line-soft);
  background:
    linear-gradient(var(--hero-grid) 1px, transparent 1px),
    linear-gradient(90deg, var(--hero-grid) 1px, transparent 1px),
    rgba(15, 23, 42, 0.18);
  background-size: 36px 36px, 36px 36px, auto;
}

.learning-flow {
  width: 100%;
  height: 100%;
  --vf-node-color: transparent;
  --vf-node-bg: transparent;
  --vf-box-shadow: none;
}

.custom-node {
  width: 180px;
  border-radius: 20px;
  padding: 14px;
  border: 1px solid transparent;
  background: rgba(15, 23, 42, 0.86);
  box-shadow: 0 18px 32px rgba(2, 6, 23, 0.28);
  color: #f8fbff;
  display: grid;
  gap: 10px;
  transition:
    transform var(--transition-fast),
    border-color var(--transition-fast),
    box-shadow var(--transition-fast),
    opacity var(--transition-fast);

  strong {
    font-size: 16px;
    line-height: 1.3;
  }

  p {
    margin: 0;
    color: rgba(226, 232, 240, 0.82);
    font-size: 12px;
    line-height: 1.55;
  }

  &.track-roadmap {
    background: linear-gradient(180deg, rgba(15, 23, 42, 0.95), rgba(18, 76, 151, 0.92));
  }

  &.track-knowledge {
    background: linear-gradient(180deg, rgba(15, 23, 42, 0.95), rgba(91, 33, 182, 0.92));
  }

  &.related {
    border-color: rgba(148, 163, 184, 0.25);
  }

  &.selected {
    transform: translateY(-2px);
    border-color: rgba(34, 197, 94, 0.7);
    box-shadow: 0 0 0 1px rgba(34, 197, 94, 0.32), 0 18px 32px rgba(2, 6, 23, 0.36);
  }
}

.node-top,
.node-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.node-kind {
  font-size: 11px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: rgba(186, 230, 253, 0.9);
}

.node-time {
  font-size: 12px;
  color: rgba(226, 232, 240, 0.84);
}

.node-meta {
  color: rgba(191, 219, 254, 0.82);
  font-size: 11px;
}

:deep(.vue-flow__node-learning) {
  background: transparent;
  border: none;
  padding: 0;
}

:deep(.vue-flow__handle) {
  opacity: 0;
}

:deep(.vue-flow__edge-path) {
  transition:
    stroke var(--transition-fast),
    stroke-width var(--transition-fast),
    opacity var(--transition-fast);
}

:deep(.vue-flow__edge-text) {
  fill: var(--text-muted);
  font-size: 11px;
}

@media (max-width: 1080px) {
  .panel-head {
    flex-direction: column;
  }

  .map-surface {
    height: 520px;
  }
}

@media (max-width: 768px) {
  .map-panel {
    padding: 20px;
  }

  .map-surface {
    height: 460px;
  }

  .custom-node {
    width: 156px;
  }
}
</style>
