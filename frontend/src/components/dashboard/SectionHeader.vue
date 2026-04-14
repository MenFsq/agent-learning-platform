<template>
  <div class="section-header">
    <div>
      <p v-if="eyebrow" class="section-eyebrow">{{ eyebrow }}</p>
      <h2 class="section-title">{{ title }}</h2>
      <p v-if="description" class="section-description">{{ description }}</p>
    </div>

    <router-link v-if="actionLabel && actionHref" :to="actionHref" class="section-action">
      {{ actionLabel }}
    </router-link>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  eyebrow?: string
  title: string
  description?: string
  actionLabel?: string
  actionHref?: string
}>()
</script>

<style scoped lang="scss">
.section-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 16px;
}

.section-eyebrow {
  margin: 0 0 10px;
  font-size: 11px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--color-secondary);
}

.section-title {
  margin: 0;
  font-size: clamp(24px, 2vw, 30px);
  line-height: 1.15;
  color: var(--text-primary);
}

.section-description {
  max-width: 620px;
  margin: 12px 0 0;
  color: var(--text-secondary);
  line-height: 1.7;
}

.section-action {
  flex-shrink: 0;
  color: var(--text-secondary);
  transition:
    transform var(--transition-fast),
    color var(--transition-fast);

  &:hover {
    color: var(--text-primary);
    transform: translateX(2px);
  }
}

@media (max-width: 768px) {
  .section-header {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
