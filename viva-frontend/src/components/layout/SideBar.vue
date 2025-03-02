<template>
  <nav class="sidebar">
    <div class="sidebar-content">
      <div class="logo">
        <img src="/logo.png" alt="DejaVu Logo">
      </div>
      <ul class="nav-list">
        <li>
          <router-link to="/" exact class="nav-item">
            <span class="material-symbols-outlined">home</span>
            <span>Feedback</span>
          </router-link>
        </li>
        <li>
          <a href="#" @click.prevent="$emit('openAddEssay')" class="nav-item">
            <span class="material-symbols-outlined">add_circle</span>
            <span>Publish</span>
          </a>
        </li>
        <li>
          <router-link to="/review" class="nav-item">
            <span class="material-symbols-outlined">notifications</span>
            <span>Review</span>
          </router-link>
        </li>
        <li>
          <a href="#" class="nav-item" @click.prevent="$emit('openSubscribe')">
            <span class="material-symbols-outlined">workspace_premium</span>
            <span>Subscribe</span>
          </a>
        </li>
        <li>
          <a href="#" class="nav-item" @click.prevent="showSettings = true">
            <span class="material-symbols-outlined">person</span>
            <span>Me</span>
            <span class="new-badge">PRO</span>
          </a>
        </li>

        <li class="login-button-wrapper">
          <LoginButton/>
        </li>
      </ul>
    </div>
    <SettingsModal v-model="showSettings" />
  </nav>
</template>

<script>
import LoginButton from '@/components/layout/LoginButton.vue'
import SettingsModal from '@/components/layout/SettingsModal.vue'

export default {
  name: 'Sidebar',
  components: {
    LoginButton,
    SettingsModal
  },
  data() {
    return {
      showSettings: false
    }
  },
  emits: ['openAddEssay', 'openSubscribe']
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

.sidebar {
  display: flex;
  flex-direction: column;
  width: 250px;
  background-color: #FFFFFF;
  border-right: none;
  position: fixed;
  height: 100vh;
  overflow: hidden;
}

.nav-list {
  list-style: none;
  padding: 16px 0;
  margin: 0;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 12px 24px;
  color: #333;
  text-decoration: none;
  position: relative;
  font-weight: bold;
  transition: all 0.2s ease;
  font-size: 12px;
  font-style: inherit;
  margin: 4px 16px;
  border-radius: 8px;
  box-shadow: none;
}

.nav-item:hover {
  background-color: #f7f7f7;
}

.router-link-exact-active {
  background-color: #f7f7f7;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.nav-item .material-symbols-outlined {
  font-size: 24px;
  margin-right: 12px;
  font-variation-settings:
    'FILL' 0,
    'wght' 400,
    'GRAD' 0,
    'opsz' 24;
}

.nav-item span:not(.material-symbols-outlined) {
  font-size: 20px;
}

.logo {
  padding-top: 30px;
  text-align: center;
}

.logo img {
  height: auto;
  width: 210px;
  max-width: 300px;
}

/* NEW badge styles */
.new-badge {
  background-color: var(--color-primary);
  color: white;
  font-size: 13px;
  padding: 2px 6px;
  border-radius: 6px;
  margin-left: 8px;
  font-weight: 500;
  display: inline-block;
  line-height: 1.2;
  vertical-align: middle;
}

/* 深色模式 */
@media (prefers-color-scheme: dark) {
  .sidebar {
    background-color: #1a1a1a;
  }
  
  .nav-item {
    color: #ffffff;
  }

  .nav-item:hover,
  .router-link-exact-active {
    background-color: rgba(255, 255, 255, 0.05);
  }
}

.login-button-wrapper {
  margin-top: auto;
  padding: 0 16px;
}

.login-button-wrapper :deep(.login-container) {
  padding: 8px;
}
</style>
