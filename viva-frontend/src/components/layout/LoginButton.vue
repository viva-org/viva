<template>
  <div class="login-container">
    <!-- 未登录状态显示登录按钮 -->
    <template v-if="!userStore.isLoggedIn">
      <div id="g_id_onload"
           data-client_id="145000233203-68qjqeimootonnuv999os54ni9s0k14g.apps.googleusercontent.com"
           data-context="signin"
           data-ux_mode="popup"
           data-callback="handleCredentialResponse"
           data-auto_select="false"
           data-auto_prompt="false">
      </div>

      <div class="g_id_signin bento-card"
           data-type="standard"
           data-shape="rectangular"
           data-theme="outline"
           data-text="signin_with"
           data-size="large"
           data-logo_alignment="left">
      </div>
    </template>

    <!-- 登录状态显示用户头像 -->
    <template v-else>
      <div class="user-avatar" @click="handleAvatarClick">
        <div class="avatar-wrapper">
          <img 
            v-if="userStore.user?.picture" 
            :src="userStore.user.picture" 
            :alt="userStore.user?.name || 'User avatar'"
            @error="handleImageError"
            ref="avatarImg"
          />
          <div v-else class="avatar-fallback">
            {{ getUserInitials() }}
          </div>
        </div>
        <span class="user-name">{{ userStore.user?.name }}</span>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'
import api from '@/services/api'

// 组件状态
const router = useRouter()
const userStore = useUserStore()
const avatarImg = ref(null)
const googleClientId = '145000233203-68qjqeimootonnuv999os54ni9s0k14g.apps.googleusercontent.com'

// 方法
const handleAvatarClick = () => {
  // 可以添加点击头像后的操作，比如显示下拉菜单
  console.log('Avatar clicked')
}

const handleImageError = () => {
  if (avatarImg.value) {
    avatarImg.value.src = '/default-avatar.png'
  }
}

const getUserInitials = () => {
  if (!userStore.user?.name) return '?'
  return userStore.user.name
    .split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

const handleCredentialResponse = async (response) => {
  try {
    const result = await api.verifyGoogleToken(response.credential)
    userStore.setUser(result.user)
    userStore.setLoggedIn(true)
    router.push('/')
  } catch (error) {
    console.error('Login failed:', error)
    // 检查是否是认证错误
    if (error.response?.data?.detail === 'Could not validate credentials') {
      // 清除本地存储的认证信息
      localStorage.removeItem('jwt_token')
      userStore.logout()
      
      // 重新初始化 Google 登录按钮
      if (window.google?.accounts) {
        window.google.accounts.id.prompt()
      }
      
      // 可以使用你喜欢的提示方式，这里用 alert 作为示例
      alert('登录已过期，请重新登录')
    }
  }
}

// 生命周期钩子
onMounted(() => {
  window.handleCredentialResponse = handleCredentialResponse

  const script = document.createElement('script')
  script.src = 'https://accounts.google.com/gsi/client'
  script.async = true
  script.defer = true
  script.onload = () => {
    if (window.google?.accounts) {
      window.google.accounts.id.initialize({
        client_id: googleClientId,
        callback: window.handleCredentialResponse,
        auto_select: false,
        cancel_on_tap_outside: true,
        itp_support: true
      })
    }
  }
  document.head.appendChild(script)
})
</script>

<style scoped>
.user-avatar {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.avatar-wrapper {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  overflow: hidden;
  background-color: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-fallback {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #1a73e8;
  color: white;
  font-weight: 500;
  font-size: 14px;
}

.user-name {
  font-size: 14px;
  color: #333;
}

/* 深色模式 */
@media (prefers-color-scheme: dark) {
  .avatar-wrapper {
    background-color: #333;
  }
  
  .user-name {
    color: #fff;
  }
  
  .user-avatar:hover {
    background-color: rgba(255, 255, 255, 0.1);
  }
}

.login-container {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: transparent;
}

/* 深色模式 */
@media (prefers-color-scheme: dark) {
  .login-container {
    background-color: transparent;
  }
}
</style>