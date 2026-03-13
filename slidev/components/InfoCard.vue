<template>
  <div class="info-card" :class="`card-${color}`">
    <div class="card-header">
      <span class="card-icon">{{ icon }}</span>
      <span class="card-title">{{ title }}</span>
    </div>
    <div class="card-subtitle">
      <slot name="subtitle" />
    </div>
    <div class="card-body">
      <slot />
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  icon: String,
  color: {
    type: String,
    default: 'cyan'
  }
})
</script>

<style scoped>
.info-card {
  background: var(--slide-bg-card);
  border-radius: 0.6rem;
  padding: 1.1rem 1.2rem;
  border-top: 3px solid;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.card-cyan   { border-color: var(--accent-cyan); }
.card-purple { border-color: var(--accent-purple); }
.card-orange { border-color: var(--accent-orange); }
.card-pink   { border-color: var(--accent-pink); }
.card-green  { border-color: var(--accent-green); }

.card-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.card-icon {
  font-size: 1.1rem;
}

.card-title {
  font-weight: 700;
  font-size: 0.9rem;
  color: var(--slide-fg);
}

.card-cyan   .card-title { color: var(--accent-cyan); }
.card-purple .card-title { color: var(--accent-purple); }
.card-orange .card-title { color: var(--accent-orange); }
.card-pink   .card-title { color: var(--accent-pink); }
.card-green  .card-title { color: var(--accent-green); }

.card-subtitle {
  font-size: 0.72rem;
  color: var(--slide-muted);
  font-style: italic;
}

.card-body {
  font-size: 0.78rem;
  color: var(--slide-fg);
  line-height: 1.55;
}

.card-body :deep(ul) {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.card-body :deep(li) {
  padding-left: 1.4em;
  text-indent: -1.4em;
}

.card-body :deep(li)::before {
  content: '→ ';
  color: var(--slide-muted);
}
</style>
