<template>
  <Transition name="toast">
    <div v-if="show" class="toast" :class="type">
      <div class="toast-content">
        <i v-if="type === 'success'" class="mdi mdi-check-circle"></i>
        <i v-else-if="type === 'error'" class="mdi mdi-alert-circle"></i>
        <i v-else-if="type === 'warning'" class="mdi mdi-alert"></i>
        <span>{{ message }}</span>
      </div>
    </div>
  </Transition>
</template>

<script setup>
defineProps({
  show: Boolean,
  message: String,
  type: {
    type: String,
    default: 'info'  // 'success', 'error', 'warning', 'info'
  }
})
</script>

<style scoped>
.toast {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 12px 24px;
  border-radius: 8px;
  color: white;
  font-size: 14px;
  z-index: 9999;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
  min-width: 250px;
  max-width: 400px;
}

.toast-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

.toast i {
  font-size: 18px;
}

.success {
  background-color: #4caf50;
}

.error {
  background-color: #f44336;
}

.warning {
  background-color: #ff9800;
}

.info {
  background-color: #2196f3;
}

/* 动画效果 */
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateY(-30px);
}

/* 深色模式适配 */
@media (prefers-color-scheme: dark) {
  .toast {
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.3);
  }
}
</style>
