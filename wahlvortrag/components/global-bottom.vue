<script setup>
import { useNav } from '@slidev/client'
const { currentPage, total } = useNav()
</script>

<template>
  <div class="global-footer" role="contentinfo" aria-label="Footer: Anton Stadler - Event-Driven Architecture, 2026-03-20, page number">
    <span class="footer-slash">//</span>
    Anton Stadler | Event-Driven Architecture | 2026-03-20
    <span class="footer-spacer" />
    <span class="footer-num">{{ String(currentPage).padStart(2, '0') }}</span>
    <span class="footer-sep"> / </span>
    <span class="footer-total">{{ String(total).padStart(2, '0') }}</span>
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
</style>
