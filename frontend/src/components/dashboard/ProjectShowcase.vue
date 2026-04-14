<template>
  <section class="project-section reveal" data-reveal>
    <SectionHeader
      eyebrow="Continue Building"
      title="我的项目 · 继续创作"
      description="保留你的核心开发上下文，把最近推进的 Agent 项目和下一步动作放在一屏内。"
      action-label="查看全部"
      action-href="/projects"
    />

    <div class="project-grid">
      <article v-for="project in items" :key="project.id" class="project-card">
        <div class="project-top">
          <div>
            <span class="project-status" :class="project.statusTone">{{ project.status }}</span>
            <h3>{{ project.name }}</h3>
            <p>{{ project.summary }}</p>
          </div>
          <router-link :to="`/projects`" class="project-link">查看</router-link>
        </div>

        <div class="project-progress">
          <div class="progress-row">
            <span>进度</span>
            <span class="metric-mono">{{ project.progress }}%</span>
          </div>
          <div class="progress-bar">
            <span :style="{ width: `${project.progress}%` }"></span>
          </div>
        </div>

        <div class="project-bottom">
          <div class="member-stack">
            <span
              v-for="member in project.members"
              :key="member.name"
              class="member-avatar"
              :style="{ backgroundImage: `url(${member.avatar})` }"
            ></span>
          </div>
          <span class="project-update">更新于 {{ project.updatedAt }}</span>
        </div>
      </article>
    </div>
  </section>
</template>

<script setup lang="ts">
import SectionHeader from './SectionHeader.vue'
import type { ProjectItem } from './types'

defineProps<{
  items: ProjectItem[]
}>()
</script>

<style scoped lang="scss">
@use '@/styles/mixins' as *;

.project-section {
  display: grid;
  gap: 18px;
}

.project-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
}

.project-card {
  @include section-shell;
  @include panel-hover;
  padding: 24px;
  display: grid;
  gap: 22px;
}

.project-top {
  display: flex;
  justify-content: space-between;
  gap: 16px;

  h3 {
    margin: 14px 0 8px;
    font-size: 22px;
    color: var(--text-primary);
  }

  p {
    margin: 0;
    color: var(--text-secondary);
    line-height: 1.7;
  }
}

.project-status {
  display: inline-flex;
  align-items: center;
  padding: 6px 12px;
  border-radius: 999px;
  font-size: 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  border: 1px solid transparent;

  &.primary {
    color: #9bd0ff;
    background: rgba(59, 130, 246, 0.14);
    border-color: rgba(59, 130, 246, 0.24);
  }

  &.success {
    color: #8ce5a0;
    background: rgba(34, 197, 94, 0.14);
    border-color: rgba(34, 197, 94, 0.24);
  }

  &.warning {
    color: #f8cf8a;
    background: rgba(245, 158, 11, 0.14);
    border-color: rgba(245, 158, 11, 0.24);
  }
}

.project-link {
  align-self: flex-start;
  color: var(--text-secondary);
  transition:
    transform var(--transition-fast),
    color var(--transition-fast);

  &:hover {
    color: var(--text-primary);
    transform: translateX(2px);
  }
}

.progress-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
  color: var(--text-secondary);
}

.progress-bar {
  position: relative;
  height: 8px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.06);
  overflow: hidden;

  span {
    display: block;
    height: 100%;
    border-radius: inherit;
    background: linear-gradient(90deg, var(--color-primary), var(--color-accent));
    box-shadow: 0 0 16px rgba(59, 130, 246, 0.26);
  }
}

.project-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.member-stack {
  display: flex;
}

.member-avatar {
  width: 34px;
  height: 34px;
  border-radius: 999px;
  border: 2px solid var(--app-bg-elevated);
  background-size: cover;
  background-position: center;
  margin-left: -10px;

  &:first-child {
    margin-left: 0;
  }
}

.project-update {
  color: var(--text-muted);
  font-size: 13px;
}

@media (max-width: 900px) {
  .project-grid {
    grid-template-columns: 1fr;
  }
}
</style>
