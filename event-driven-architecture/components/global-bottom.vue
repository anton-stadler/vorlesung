<script setup>
import { computed, ref } from 'vue'
import { useNav } from '@slidev/client'
const { currentPage, slides, go } = useNav()

const mainSlides = computed(() =>
  slides.value.filter(s => !s.meta?.slide?.frontmatter?.backup)
)
const mainTotal = computed(() => mainSlides.value.length)
const displayPage = computed(() =>
  Math.min(currentPage.value, mainTotal.value)
)

const showPicker = ref(false)
function goToSlide(no) {
  go(no)
  showPicker.value = false
}
</script>

<template>
  <div class="global-footer" role="contentinfo" aria-label="Footer: Anton Stadler - Scalable Systems with Event-Driven Architecture, 2026-03-20, page number">
    <!-- Backdrop -->
    <div v-if="showPicker" class="picker-backdrop" @click="showPicker = false" />
    <!-- Slide Picker -->
    <div v-if="showPicker" class="picker-popup">
      <button
        v-for="slide in mainSlides"
        :key="slide.no"
        class="picker-row"
        :class="{ 'picker-row--active': slide.no === currentPage }"
        @click="goToSlide(slide.no)"
      >
        <span class="picker-no">{{ String(slide.no).padStart(2, '0') }}</span>
        <span class="picker-alias">{{ slide.meta?.slide?.frontmatter?.routeAlias ?? '—' }}</span>
      </button>
    </div>

    <span class="footer-slash">//</span>
    Anton Stadler | Scalable Systems with Event-Driven Architecture | 2026-03-20
    <span class="footer-spacer" />
    <button class="footer-btn footer-demo" @click="go('demo')" title="Go to Demo">Demo</button>
    <button class="footer-btn" @click="go(currentPage - 1)" title="Previous slide">◀</button>
    <span
      class="footer-num footer-num--clickable"
      :class="{ 'footer-num--open': showPicker }"
      title="Slide picker"
      @click="showPicker = !showPicker"
    >{{ String(displayPage).padStart(2, '0') }}</span>
    <span class="footer-sep"> / </span>
    <span class="footer-total">{{ String(mainTotal).padStart(2, '0') }}</span>
    <button class="footer-btn" @click="go(currentPage + 1)" title="Next slide">▶</button>
  </div>
</template>

<style scoped>
.global-footer {
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

.footer-num--clickable {
  cursor: pointer;
  border-radius: 3px;
  padding: 0.1rem 0.25rem;
  transition: background 0.15s, color 0.15s;
}
.footer-num--clickable:hover,
.footer-num--open {
  background: rgba(0, 123, 170, 0.12);
  color: var(--accent-cyan, #007BAA);
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

/* Backdrop */
.picker-backdrop {
  position: fixed;
  inset: 0;
  z-index: 49;
}

/* Slide Picker Popup */
.picker-popup {
  position: absolute;
  bottom: calc(100% + 0.3rem);
  right: 2rem;
  z-index: 50;
  background: var(--slide-bg, #F8F8F4);
  border: 1px solid var(--slide-border, #CBD5E1);
  border-radius: 8px;
  padding: 0.4rem;
  box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  min-width: 11rem;
  max-height: 22rem;
  overflow-y: auto;
}

.picker-row {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.3rem 0.6rem;
  border: 1px solid transparent;
  border-radius: 4px;
  background: none;
  cursor: pointer;
  font-family: 'JetBrains Mono', 'Consolas', monospace;
  font-size: 0.65rem;
  color: var(--slide-muted, #5A6A8A);
  text-align: left;
  transition: background 0.12s, border-color 0.12s, color 0.12s;
  white-space: nowrap;
}
.picker-row:hover {
  background: rgba(0, 123, 170, 0.08);
  border-color: var(--accent-cyan, #007BAA);
  color: var(--accent-cyan, #007BAA);
}
.picker-row--active {
  background: rgba(0, 123, 170, 0.12);
  border-color: var(--accent-cyan, #007BAA);
  color: var(--accent-cyan, #007BAA);
  font-weight: 700;
}

.picker-no {
  opacity: 0.5;
  min-width: 1.4rem;
}
.picker-row--active .picker-no,
.picker-row:hover .picker-no {
  opacity: 0.7;
}

.picker-alias {
  letter-spacing: 0.03em;
}
</style>
