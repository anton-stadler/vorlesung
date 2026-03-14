<script setup>
import GlobalBottom from '../components/global-bottom.vue'

const props = defineProps({
  class: {
    type: String,
  },
  layoutClass: {
    type: String,
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
  grid-area: 3 / 1 / 3 / 3;
}
</style>
