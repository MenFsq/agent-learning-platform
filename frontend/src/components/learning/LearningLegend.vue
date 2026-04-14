<template>
  <section class="legend-card">
    <div class="legend-head">
      <p class="eyebrow">地图说明</p>
      <h3>如何阅读这张地图</h3>
    </div>

    <div class="legend-grid">
      <div class="legend-item">
        <span class="legend-swatch roadmap"></span>
        <div>
          <strong>学习阶段</strong>
          <p>表示推荐的推进顺序和阶段目标。</p>
        </div>
      </div>
      <div class="legend-item">
        <span class="legend-swatch knowledge"></span>
        <div>
          <strong>知识节点</strong>
          <p>表示你需要掌握的概念模块和关键能力。</p>
        </div>
      </div>
      <div class="legend-item">
        <span class="legend-swatch active"></span>
        <div>
          <strong>当前聚焦</strong>
          <p>点击任意节点后，会同步更新详情、阶段和资源视图。</p>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped lang="scss">
@use '@/styles/mixins' as *;

.legend-card {
  @include section-shell;
  padding: 20px;
  display: grid;
  gap: 18px;
}

.legend-head {
  display: grid;
  gap: 8px;

  h3 {
    margin: 0;
    font-size: 20px;
  }
}

.eyebrow {
  margin: 0;
  color: var(--color-secondary);
  font-size: 11px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
}

.legend-grid {
  display: grid;
  gap: 14px;
}

.legend-item {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 12px;
  align-items: start;

  strong {
    display: block;
    margin-bottom: 4px;
    color: var(--text-primary);
  }

  p {
    margin: 0;
    color: var(--text-secondary);
    line-height: 1.6;
  }
}

.legend-swatch {
  width: 14px;
  height: 14px;
  border-radius: 999px;
  margin-top: 3px;

  &.roadmap {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.95), rgba(6, 182, 212, 0.95));
  }

  &.knowledge {
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.95), rgba(236, 72, 153, 0.95));
  }

  &.active {
    background: linear-gradient(135deg, rgba(34, 197, 94, 0.95), rgba(16, 185, 129, 0.95));
  }
}
</style>
