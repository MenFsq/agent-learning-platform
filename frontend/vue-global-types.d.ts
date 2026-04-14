declare global {
  const defineProps: typeof import('vue')['defineProps']
  const defineEmits: typeof import('vue')['defineEmits']
  const defineExpose: typeof import('vue')['defineExpose']
  const defineOptions: typeof import('vue')['defineOptions']
  const defineSlots: typeof import('vue')['defineSlots']
  const defineModel: typeof import('vue')['defineModel']
  const withDefaults: typeof import('vue')['withDefaults']
}

export {}
