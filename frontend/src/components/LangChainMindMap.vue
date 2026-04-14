<template>
  <section class="learning-workbench">
    <div class="workspace-grid">
      <div class="main-stack">
        <LearningMapCanvas
          ref="mapRef"
          :nodes="learningNodes"
          :connections="learningConnections"
          :selected-node-id="selectedNode.id"
          @select-node="selectNode"
        />

        <LearningStagePanel
          :stages="learningStages"
          :nodes="learningNodes"
          :selected-stage-id="selectedStage.id"
          :current-node-id="selectedNode.id"
          @select-node="selectNode"
        />
      </div>

      <div class="side-stack">
        <LearningLegend />
        <LearningNodeDetail
          :node="selectedNode"
          :stage="selectedStage"
          :all-nodes="learningNodes"
          @select-node="selectNode"
        />
      </div>
    </div>

    <LearningResourcePanel
      :resources="secondaryResources"
      :featured-resources="featuredResources"
      :selected-node-title="selectedNode.shortTitle"
    />
  </section>
</template>

<script setup lang="ts">
import { computed, nextTick, ref } from 'vue'

import LearningLegend from '@/components/learning/LearningLegend.vue'
import LearningMapCanvas from '@/components/learning/LearningMapCanvas.vue'
import LearningNodeDetail from '@/components/learning/LearningNodeDetail.vue'
import LearningResourcePanel from '@/components/learning/LearningResourcePanel.vue'
import LearningStagePanel from '@/components/learning/LearningStagePanel.vue'
import {
  defaultSelectedNodeId,
  learningConnections,
  learningNodes,
  learningResources,
  learningStages,
  learningStageMap,
  learningNodeMap,
  type LearningResource,
  type LearningAction
} from '@/data/learning/langchainCurriculum'

const mapRef = ref<{
  focusSelectedNode?: () => Promise<boolean> | void
  fitMap?: () => Promise<boolean> | void
} | null>(null)

const selectedNodeId = ref(defaultSelectedNodeId)

const selectedNode = computed(() => learningNodeMap[selectedNodeId.value] ?? learningNodes[0])
const selectedStage = computed(() => learningStageMap[selectedNode.value.stageId] ?? learningStages[0])

const featuredResources = computed(() => selectedNode.value.resources)

const secondaryResources = computed(() => {
  const featuredIds = new Set(featuredResources.value.map((resource: LearningResource) => resource.id))
  return learningResources.filter((resource: LearningResource) => !featuredIds.has(resource.id))
})

const selectNode = async (nodeId: string) => {
  if (!learningNodeMap[nodeId]) {
    return
  }

  selectedNodeId.value = nodeId
  await nextTick()
}

const focusNode = async (nodeId: string) => {
  await selectNode(nodeId)
  await mapRef.value?.focusSelectedNode?.()
}

const scrollToSection = (sectionId: string) => {
  document.getElementById(sectionId)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

const runAction = async (action: LearningAction) => {
  await focusNode(action.targetNodeId)
  scrollToSection(action.sectionId)
}

defineExpose({
  focusNode,
  runAction,
  scrollToSection
})
</script>

<style scoped lang="scss">
.learning-workbench {
  display: grid;
  gap: 24px;
}

.workspace-grid {
  display: grid;
  gap: 24px;
  grid-template-columns: minmax(0, 1.65fr) minmax(320px, 0.82fr);
  align-items: start;
}

.main-stack,
.side-stack {
  display: grid;
  gap: 20px;
}

.side-stack {
  align-content: start;
}

@media (max-width: 1200px) {
  .workspace-grid {
    grid-template-columns: 1fr;
  }
}
</style>
