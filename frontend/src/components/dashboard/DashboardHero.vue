<template>
  <section class="hero-panel reveal" data-reveal>
    <div class="hero-copy">
      <p class="hero-eyebrow">One Workspace For AI Builders</p>
      <h1 class="hero-title">
        欢迎回来，<span class="text-gradient">{{ userName }}</span>
      </h1>
      <p class="hero-subtitle">{{ subtitle }}</p>

      <div class="hero-metrics">
        <div v-for="item in metrics" :key="item.label" class="metric-chip">
          <AnimatedNumber :value="item.value" :suffix="item.suffix" />
          <span>{{ item.label }}</span>
        </div>
      </div>

      <div class="hero-actions">
        <router-link to="/" class="hero-button primary">进入工作台</router-link>
        <router-link to="/projects" class="hero-button secondary">快速新建</router-link>
      </div>
    </div>

    <div class="hero-visual">
      <div class="visual-grid"></div>
      <div class="visual-orb orb-a"></div>
      <div class="visual-orb orb-b"></div>

      <div class="hero-surface main-surface">
        <span class="surface-label">Current Flow</span>
        <strong>Agent 构建、学习、部署一屏协作</strong>
        <p>将项目、学习路径和社区线索压缩到一个持续可用的 AI 工作台。</p>
      </div>

      <div v-for="item in highlights" :key="item.title" class="hero-surface mini-surface">
        <span class="surface-label">{{ item.title }}</span>
        <strong>{{ item.value }}</strong>
        <p>{{ item.detail }}</p>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import AnimatedNumber from './AnimatedNumber.vue'
import type { HeroMetric } from './types'

defineProps<{
  userName: string
  subtitle: string
  metrics: HeroMetric[]
  highlights: Array<{
    title: string
    value: string
    detail: string
  }>
}>()
</script>

<style scoped lang="scss">
@use '@/styles/mixins' as *;

.hero-panel {
  @include section-shell;
  display: grid;
  grid-template-columns: minmax(0, 1.15fr) minmax(320px, 0.85fr);
  gap: clamp(28px, 4vw, 44px);
  padding: clamp(28px, 4vw, 40px);
}

.hero-panel::after {
  content: '';
  position: absolute;
  inset: auto 10% 0 auto;
  width: 240px;
  height: 240px;
  border-radius: 999px;
  background: radial-gradient(circle, rgba(59, 130, 246, 0.18), transparent 70%);
  filter: blur(8px);
}

.hero-copy,
.hero-visual {
  position: relative;
  z-index: 1;
}

.hero-copy {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 22px;
}

.hero-eyebrow {
  margin: 0;
  font-size: 12px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--color-secondary);
}

.hero-title {
  margin: 0;
  font-size: clamp(40px, 6vw, 68px);
  line-height: 0.98;
  letter-spacing: -0.04em;
  color: var(--text-primary);
}

.hero-subtitle {
  max-width: 620px;
  margin: 0;
  font-size: clamp(16px, 2vw, 19px);
  line-height: 1.75;
  color: var(--text-secondary);
}

.hero-metrics {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.metric-chip {
  @include glass-panel(rgba(255, 255, 255, 0.04), var(--line-soft));
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  border-radius: 999px;
  color: var(--text-secondary);

  span:first-child {
    font-size: 18px;
    font-weight: 600;
    color: var(--text-primary);
  }
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
}

.hero-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 144px;
  min-height: 48px;
  padding: 0 20px;
  border-radius: 999px;
  border: 1px solid var(--line-strong);
  transition:
    transform var(--transition-fast),
    box-shadow var(--transition-fast),
    border-color var(--transition-fast),
    background var(--transition-fast);

  &:hover {
    transform: translateY(-2px);
  }
}

.hero-button.primary {
  color: #ffffff;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.96), rgba(6, 182, 212, 0.9));
  box-shadow: 0 20px 36px rgba(59, 130, 246, 0.26);
}

.hero-button.secondary {
  color: var(--text-primary);
  background: transparent;
}

.hero-visual {
  min-height: 420px;
  display: grid;
  align-content: end;
  gap: 14px;
  overflow: hidden;
}

.visual-grid {
  position: absolute;
  inset: 0;
  border-radius: calc(var(--radius-xl) - 2px);
  background-image:
    linear-gradient(var(--hero-grid) 1px, transparent 1px),
    linear-gradient(90deg, var(--hero-grid) 1px, transparent 1px);
  background-size: 42px 42px;
  mask-image: radial-gradient(circle at center, black 22%, transparent 90%);
  opacity: 0.7;
  animation: drift 16s linear infinite;
}

.visual-orb {
  position: absolute;
  border-radius: 999px;
  filter: blur(4px);
  opacity: 0.8;
  animation: float 9s ease-in-out infinite;
}

.orb-a {
  top: 12%;
  right: 14%;
  width: 180px;
  height: 180px;
  background: radial-gradient(circle, rgba(59, 130, 246, 0.4), transparent 72%);
}

.orb-b {
  bottom: 14%;
  left: 4%;
  width: 210px;
  height: 210px;
  background: radial-gradient(circle, rgba(139, 92, 246, 0.32), transparent 72%);
  animation-delay: -3s;
}

.hero-surface {
  @include glass-panel(rgba(9, 12, 20, 0.46), rgba(255, 255, 255, 0.1));
  position: relative;
  border-radius: var(--radius-lg);
  padding: 18px 18px 20px;
}

[data-theme='light'] .hero-surface {
  background: rgba(255, 255, 255, 0.78);
}

.main-surface {
  max-width: 360px;

  strong {
    display: block;
    margin-top: 12px;
    font-size: 22px;
    line-height: 1.4;
    color: var(--text-primary);
  }

  p {
    margin: 10px 0 0;
    color: var(--text-secondary);
    line-height: 1.7;
  }
}

.mini-surface {
  width: min(86%, 260px);
  margin-left: auto;

  strong {
    display: block;
    margin-top: 10px;
    font-size: 18px;
    color: var(--text-primary);
  }

  p {
    margin: 8px 0 0;
    color: var(--text-muted);
    line-height: 1.6;
    font-size: 13px;
  }
}

.surface-label {
  font-size: 11px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--color-secondary);
}

@keyframes float {
  0%,
  100% {
    transform: translate3d(0, 0, 0);
  }

  50% {
    transform: translate3d(0, -12px, 0);
  }
}

@keyframes drift {
  from {
    transform: translate3d(0, 0, 0);
  }

  to {
    transform: translate3d(42px, 42px, 0);
  }
}

@media (max-width: 1100px) {
  .hero-panel {
    grid-template-columns: 1fr;
  }

  .hero-visual {
    min-height: 340px;
  }
}

@media (max-width: 640px) {
  .hero-panel {
    padding: 24px;
  }

  .hero-title {
    font-size: 38px;
  }

  .hero-visual {
    min-height: 280px;
  }

  .mini-surface {
    width: 100%;
  }
}
</style>
