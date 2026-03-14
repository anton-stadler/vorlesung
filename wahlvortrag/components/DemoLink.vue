<script setup>
import { useNav } from '@slidev/client'

/** Ziel-Foliennummer der Live-Demo (1-basiert). Bei Umordnung der Folien hier anpassen. */
const DEMO_SLIDE = 3

const { go } = useNav()

function goToDemo() {
  go(DEMO_SLIDE)
}
</script>

<template>
  <button
    type="button"
    class="demo-link-btn"
    @click="goToDemo"
  >
    Zur Demo
  </button>
</template>

<style scoped>
.demo-link-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.5rem 1rem;
  font-family: 'JetBrains Mono', Consolas, monospace;
  font-size: 0.85rem;
  font-weight: 600;
  color: white;
  background: var(--accent-pink, #C0397A);
  border: none;
  border-radius: 6px;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(192, 57, 122, 0.35);
  transition: background 0.2s, transform 0.1s;
}

.demo-link-btn:hover {
  background: var(--accent-cyan, #007BAA);
  transform: translateY(-1px);
}

.demo-link-btn:active {
  transform: translateY(0);
}
</style>
