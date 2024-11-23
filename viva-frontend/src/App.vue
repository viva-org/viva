<template>
  <div id="app">
    <Toast 
      :show="showToast"
      :message="toastMessage"
      :type="toastType"
    />
    <router-view></router-view>
    <!-- 添加登录提醒对话框 -->
    <div v-if="showLoginPrompt" class="login-prompt-overlay">
      <div class="login-prompt-modal">
        <h3>登录即将过期</h3>
        <p>为了保持您的登录状态，请重新登录</p>
        <div class="login-prompt-actions">
          <button @click="handleRelogin">重新登录</button>
          <button @click="closeLoginPrompt">稍后</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useUserStore } from '@/stores/user'
// import { checkTokenExpiration } from '@/services/auth'
import Toast from '@/components/layout/Toast.vue'

const showToast = ref(false)
const toastMessage = ref('')
const toastType = ref('error')
const showLoginPrompt = ref(false)
const checkInterval = ref(null)

const userStore = useUserStore()

// // 检查登录状态
// const checkLoginStatus = () => {
//   if (userStore.isLoggedIn && checkTokenExpiration()) {
//     showLoginPrompt.value = true
//   }
// }

// // 处理重新登录
// const handleRelogin = () => {
//   if (window.google?.accounts) {
//     window.google.accounts.id.prompt()
//   }
//   showLoginPrompt.value = false
// }

// // 关闭提示
// const handleClosePrompt = () => {
//   showLoginPrompt.value = false
// }

// onMounted(() => {
//   userStore.initializeStore()
//   window.addEventListener('show-toast', handleToast)
  
//   // 每分钟检查一次登录状态
//   checkInterval.value = setInterval(checkLoginStatus, 60000)
// })

onUnmounted(() => {
  window.removeEventListener('show-toast', handleToast)
  if (checkInterval.value) {
    clearInterval(checkInterval.value)
  }
})
</script>

<style scoped>
.login-prompt-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.login-prompt-modal {
  background: white;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
  max-width: 400px;
  width: 90%;
}

.login-prompt-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 20px;
}

.login-prompt-actions button {
  padding: 8px 16px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
}

.login-prompt-actions button:first-child {
  background: #1a73e8;
  color: white;
}

.login-prompt-actions button:last-child {
  background: #f1f3f4;
  color: #3c4043;
}

/* 深色模式 */
@media (prefers-color-scheme: dark) {
  .login-prompt-modal {
    background: #1a1a1a;
    color: white;
  }

  .login-prompt-actions button:last-child {
    background: #333;
    color: white;
  }
}
</style>
