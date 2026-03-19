<script setup>
import { computed } from 'vue'
import { useNav } from '@slidev/client'
const { currentPage, slides, go, next, prev } = useNav()

const mainTotal = computed(() =>
  slides.value.filter(s => !s.meta?.slide?.frontmatter?.backup).length
)
const displayPage = computed(() =>
  Math.min(currentPage.value, mainTotal.value)
)
</script>

<template>
  <div class="global-footer" role="contentinfo" aria-label="Footer: Anton Stadler - Scalable Systems with Event-Driven Architecture, 2026-03-20, page number">
    <span class="footer-slash">//</span>
    Anton Stadler | Scalable Systems with Event-Driven Architecture | 2026-03-20
    <span class="footer-spacer" />
    <button class="footer-btn footer-demo" @click="go('demo')" title="Go to Demo">Demo</button>
    <button class="footer-btn" @click="go(currentPage - 1)" title="Previous slide">◀</button>
    <span class="footer-num">{{ String(displayPage).padStart(2, '0') }}</span>
    <span class="footer-sep"> / </span>
    <span class="footer-total">{{ String(mainTotal).padStart(2, '0') }}</span>
    <button class="footer-btn" @click="go(currentPage + 1)" title="Next slide">▶</button>
  </div>
</template>

<style scoped>
.global-footer {
  /* Am unteren Rand der Folie, nicht des Viewports – Control-Leiste bleibt sichtbar */
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2rem;
  padding: 0 2rem;
  display: flex;
  align-items: center;
  gap: 0.5em;
  border-top: 1px solid var(--slide-border, #CCCCCC);
  background: var(--slide-bg, #F8F8F4);
  font-family: 'JetBrains Mono', 'Consolas', monospace;
  font-size: 0.62rem;
  color: var(--slide-muted, #5A6A8A);
  letter-spacing: 0.05em;
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.08);
}

.footer-slash {
  color: var(--accent-pink, #C0397A);
  font-weight: 700;
}

.footer-spacer {
  flex: 1;
}

.footer-num {
  color: var(--accent-cyan, #007BAA);
  font-weight: 700;
}

.footer-sep {
  opacity: 0.4;
}

.footer-total {
  opacity: 0.5;
}

.footer-btn {
  background: none;
  border: 1px solid var(--slide-border, #CBD5E1);
  border-radius: 4px;
  color: var(--slide-muted, #5A6A8A);
  font-family: inherit;
  font-size: 0.58rem;
  padding: 0.15rem 0.4rem;
  cursor: pointer;
  transition: background 0.15s, color 0.15s, border-color 0.15s;
  line-height: 1;
}
.footer-btn:hover {
  border-color: var(--accent-cyan, #007BAA);
  color: var(--accent-cyan, #007BAA);
}

.footer-demo {
  font-weight: 600;
  color: var(--accent-pink, #C0397A);
  border-color: var(--accent-pink, #C0397A);
  letter-spacing: 0.04em;
  margin-right: 0.5em;
}
.footer-demo:hover {
  background: var(--accent-pink, #C0397A);
  color: white;
}
</style>
