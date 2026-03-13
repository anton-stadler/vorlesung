<template>
  <div class="problem-box">
    <span class="problem-q">?</span>
    <span class="problem-text"><slot /></span>
  </div>
</template>

<style scoped>
.problem-box {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  background: rgba(var(--accent-red-rgb, 187, 34, 34), 0.08);
  border: 1.5px solid var(--accent-red);
  border-radius: 0.5rem;
  padding: 0.5rem 1rem;
  font-size: 0.85rem;
  color: var(--slide-fg);
}

.problem-q {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1.4rem;
  height: 1.4rem;
  background: var(--accent-red);
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
