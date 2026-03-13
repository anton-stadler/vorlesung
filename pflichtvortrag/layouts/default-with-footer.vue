<script setup>
import GlobalBottom from '../components/global-bottom.vue'
</script>

<template>
  <div class="slidev-layout default layout-with-footer">
    <div class="layout-slot">
      <slot />
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
.layout-slot {
  flex: 1;
  min-height: 0;
}
</style>
