<template>
  <div class="learning-page">
    <div class="page-container">
      <div class="learning-shell">
        <section class="hero-section">
          <div class="hero-copy">
            <p class="eyebrow">学习工作台</p>
            <h1 class="text-gradient">{{ learningMapMeta.title }}</h1>
            <p class="hero-description">{{ learningMapMeta.description }}</p>

            <div class="hero-actions">
              <button
                v-for="action in learningActions"
                :key="action.id"
                type="button"
                class="hero-action"
                @click="handleAction(action)"
              >
                <span>{{ action.label }}</span>
                <small>{{ action.helperText }}</small>
              </button>
            </div>
          </div>

          <div class="hero-summary">
            <p class="summary-label">你可以先这样使用</p>
            <ul>
              <li>先看阶段顺序，知道整条路线的推进节奏。</li>
              <li>再点地图节点，把概念、练习、验证和资料串起来看。</li>
            </ul>
          </div>
        </section>

        <section class="section-block">
          <SectionHeader
            eyebrow="学习概览"
            title="先建立整体坐标，再进入细节"
            description="先把阶段数、关键节点数和验证维度看清楚，后面点开地图时就不容易迷路。"
          />

          <div class="overview-grid">
            <article v-for="item in learningOverviewStats" :key="item.label" class="overview-card">
              <p class="stat-label">{{ item.label }}</p>
              <strong class="metric-mono">{{ item.value }}</strong>
              <p class="stat-detail">{{ item.detail }}</p>
            </article>
          </div>
        </section>

        <section class="section-block">
          <SectionHeader
            eyebrow="阶段节奏"
            title="推荐学习顺序"
            description="这一行不是详细说明，而是帮你快速建立推进顺序和时间预期。"
          />

          <div class="stage-rail">
            <article v-for="stage in learningStages" :key="stage.id" class="stage-pill">
              <p class="stage-pill-label">第 {{ stage.order }} 阶段</p>
              <strong>{{ stage.label }}</strong>
              <span class="metric-mono">{{ stage.duration }}</span>
            </article>
          </div>
        </section>

        <section class="section-block">
          <SectionHeader
            eyebrow="核心工作区"
            title="从地图进入内容，再从内容回到路线"
            description="左侧先看结构和路径，右侧聚焦当前节点的详细信息，下面再补阶段任务和资料。"
          />
          <LangChainMindMap ref="mindMapRef" />
        </section>

        <section class="principles-panel">
          <SectionHeader
            eyebrow="学习原则"
            title="建议一直保持的三条习惯"
            description="这些不是装饰性的提示，而是最直接影响学习质量和落地效率的工程习惯。"
          />

          <div class="principles-grid">
            <article v-for="principle in learningPrinciples" :key="principle.id" class="principle-card">
              <h3>{{ principle.title }}</h3>
              <p>{{ principle.description }}</p>
              <strong>{{ principle.emphasis }}</strong>
            </article>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

import SectionHeader from '@/components/dashboard/SectionHeader.vue'
import LangChainMindMap from '@/components/LangChainMindMap.vue'
import {
  learningActions,
  learningMapMeta,
  learningOverviewStats,
  learningPrinciples,
  learningStages,
  type LearningAction
} from '@/data/learning/langchainCurriculum'

const mindMapRef = ref<{
  runAction?: (action: LearningAction) => Promise<void> | void
} | null>(null)

const handleAction = async (action: LearningAction) => {
  await mindMapRef.value?.runAction?.(action)
}
</script>

<style scoped lang="scss">
@use '@/styles/mixins' as *;

.learning-page {
  min-height: 100%;
}

.learning-shell {
  width: min(1320px, 100%);
  margin: 0 auto;
  padding: clamp(28px, 4vw, 42px) 0 48px;
  display: grid;
  gap: 32px;
}

.hero-section,
.overview-card,
.stage-pill,
.principles-panel,
.principle-card {
  @include section-shell;
}

.hero-section {
  padding: clamp(28px, 4vw, 40px);
  display: grid;
  gap: 28px;
  grid-template-columns: minmax(0, 1.4fr) minmax(280px, 0.8fr);
  align-items: stretch;
}

.section-block {
  display: grid;
  gap: 18px;
}

.eyebrow,
.summary-label,
.stage-pill-label,
.stat-label {
  margin: 0;
  color: var(--color-secondary);
  font-size: 11px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
}

h1 {
  margin: 0;
  font-size: clamp(34px, 5vw, 56px);
  line-height: 1.05;
}

.hero-description {
  max-width: 760px;
  margin: 18px 0 0;
  color: var(--text-secondary);
  font-size: 17px;
  line-height: 1.8;
}

.hero-actions {
  margin-top: 24px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
  gap: 14px;
}

.hero-action {
  @include panel-hover;
  padding: 16px 18px;
  border-radius: var(--radius-lg);
  border: 1px solid var(--line-soft);
  background: rgba(255, 255, 255, 0.04);
  color: var(--text-primary);
  cursor: pointer;
  display: grid;
  gap: 6px;
  text-align: left;

  span {
    font-weight: 700;
    font-size: 16px;
  }

  small {
    color: var(--text-secondary);
    line-height: 1.6;
  }
}

.hero-summary {
  border-radius: var(--radius-xl);
  border: 1px solid var(--line-soft);
  background: rgba(255, 255, 255, 0.04);
  padding: 22px;
  display: grid;
  gap: 16px;
  align-content: start;

  ul {
    margin: 0;
    padding-left: 18px;
    color: var(--text-secondary);
    display: grid;
    gap: 12px;
    line-height: 1.7;
  }
}

.overview-grid {
  display: grid;
  gap: 14px;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
}

.overview-card {
  padding: 20px;
  display: grid;
  gap: 10px;

  strong {
    font-size: clamp(28px, 4vw, 40px);
  }
}

.stat-detail {
  margin: 0;
  color: var(--text-secondary);
  line-height: 1.7;
}

.stage-rail {
  @include hidden-scrollbar;
  display: grid;
  grid-auto-flow: column;
  grid-auto-columns: minmax(220px, 1fr);
  gap: 14px;
  overflow-x: auto;
  padding-bottom: 6px;
}

.stage-pill {
  padding: 18px;
  display: grid;
  gap: 8px;

  strong {
    font-size: 18px;
  }

  span {
    color: var(--text-secondary);
  }
}

.principles-panel {
  padding: 24px;
  display: grid;
  gap: 20px;
}

.principles-grid {
  display: grid;
  gap: 16px;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
}

.principle-card {
  @include panel-hover;
  padding: 18px;
  display: grid;
  gap: 12px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--line-soft);

  h3,
  p,
  strong {
    margin: 0;
  }

  p {
    color: var(--text-secondary);
    line-height: 1.7;
  }

  strong {
    color: var(--text-primary);
  }
}

@media (max-width: 960px) {
  .hero-section {
    grid-template-columns: 1fr;
  }
}
</style>
