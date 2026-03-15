<template>
  <div class="problem-box" :class="`problem-box--${color}`">
    <span class="problem-q">{{ icon }}</span>
    <span class="problem-text"><slot /></span>
  </div>
</template>

<script setup>
const props = defineProps({
  color: { type: String, default: 'red' },
  icon: { type: String, default: '?' },
})
</script>

<style scoped>
.problem-box {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  border-radius: 0.5rem;
  padding: 0.5rem 1rem;
  font-size: 0.85rem;
  color: var(--slide-fg);
}

.problem-box--red {
  background: rgba(187, 34, 34, 0.08);
  border: 1.5px solid var(--accent-red);
}
.problem-box--red .problem-q {
  background: var(--accent-red);
}

.problem-box--yellow {
  background: rgba(154, 119, 0, 0.08);
  border: 1.5px solid var(--accent-yellow);
}
.problem-box--yellow .problem-q {
  background: var(--accent-yellow);
}

html.dark .problem-box--yellow {
  background: rgba(241, 250, 140, 0.08);
  border-color: var(--accent-yellow);
}
html.dark .problem-box--yellow .problem-q {
  background: var(--accent-yellow);
  color: #282a36;
}

.problem-q {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1.4rem;
  height: 1.4rem;
  color: #fff;
  font-weight: 900;
  font-size: 0.85rem;
  border-radius: 0.25rem;
  flex-shrink: 0;
}

.problem-text {
  font-weight: 500;
}
</style>
