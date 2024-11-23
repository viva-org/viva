<template>
  <div class="content-area">
    <slot></slot>
  </div>
</template>

<style scoped>
.content-area {
  flex-grow: 1;
  padding: 20px;
  overflow-y: auto;
  width: 100%;
}
</style>
