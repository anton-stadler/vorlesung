<script setup>
import { useNav } from '@slidev/client'
const { go } = useNav()
</script>

<template>
  <button
    class="demo-link-btn"
    @click="go('demo')"
  >
    Demo
  </button>
</template>

<style scoped>
.demo-link-btn {
  padding: 0.35rem 0.6rem;
  background: rgba(244, 114, 182, 0.25);
  color: var(--accent-pink, #c0397a);
  border: 1px solid var(--accent-pink, #c0397a);
  border-radius: 4px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
}
.demo-link-btn:hover {
  background: var(--accent-pink, #c0397a);
  color: white;
}
</style>
