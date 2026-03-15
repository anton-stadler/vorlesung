<script setup>
import GlobalBottom from '../components/global-bottom.vue'
import DemoLink from '../components/DemoLink.vue'

const props = defineProps({
  class: {
    type: String,
  },
  layoutClass: {
    type: String,
  },
  showDemo: {
    type: Boolean,
    default: true,
  },
})
</script>

<template>
  <div class="layout-with-footer" :class="[props.class, props.layoutClass]">
    <div class="slidev-layout two-cols-header">
      <div class="col-header">
        <slot />
      </div>
      <div class="col-left">
        <slot name="left" />
      </div>
      <div class="col-right">
        <slot name="right" />
      </div>
      <div class="col-bottom">
        <slot name="bottom" />
      </div>
    </div>
    <GlobalBottom />
    <div v-if="props.showDemo" class="demo-link-wrap">
      <DemoLink />
    </div>
  </div>
</template>

<style scoped>
.layout-with-footer {
  position: relative;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.two-cols-header {
  flex: 1;
  min-height: 0;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: auto 1fr auto;
}

.col-header {
  grid-area: 1 / 1 / 2 / 3;
}

.col-left {
  grid-area: 2 / 1 / 3 / 2;
}

.col-right {
  grid-area: 2 / 2 / 3 / 3;
}

.col-bottom {
  align-self: end;
  grid-area: 3 / 1 / 4 / 3;
  margin-bottom: 0.3rem;
}

/* „Demo“ am rechten Rand, 90° gedreht, stört den Inhalt nicht */
.demo-link-wrap {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%) rotate(-90deg);
  transform-origin: center center;
  z-index: 10;
}
.demo-link-wrap :deep(.demo-link-btn) {
  white-space: nowrap;
}
</style>
