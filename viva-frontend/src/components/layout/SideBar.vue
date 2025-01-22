<template>
  <nav class="sidebar">
    <div class="sidebar-content">
      <div class="logo">Viva La Vida</div>
      <ul>

        <li>
          <router-link to="/" active-class="active">
            <i class="mdi mdi-home"></i> 刻意练习
          </router-link>
        </li>
        <li>
          <a href="#" @click.prevent="$emit('openAddEssay')">
            <i class="mdi mdi-plus"></i> 添加文章
          </a>
        </li>
        <li>
          <a href="#">
            <i class="mdi mdi-chart-line"></i> 学习进度
          </a>
        </li>
        <li>
          <router-link to="/review" active-class="active">
            <i class="mdi mdi-chart-line"></i> 单词复习
          </router-link>
        </li>
        <li>
          <a href="#">
            <i class="mdi mdi-account"></i> 我
          </a>
        </li>
        <li class="login-button-wrapper">
          <LoginButton/>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
import LoginButton from '@/components/layout/LoginButton.vue'

export default {
  name: 'Sidebar',
  components: {
    LoginButton
  },
  emits: ['openAddEssay']
}
</script>

<style scoped>
.sidebar {
  width: 280px;
  background-color: #ffffff;
  border-right: 1px solid #e8e8e8;
  position: fixed;
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.sidebar-content {
  flex: 1;
  overflow-y: auto;
  padding: 20px 0;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.sidebar ul {
  list-style-type: none;
  padding: 0;
}

.sidebar li {
  margin-bottom: 15px;
}

.sidebar a,
.sidebar router-link {
  display: flex;
  align-items: center;
  padding: 10px 20px;
  color: #333;
  text-decoration: none;
  font-weight: 500;
  transition: background-color 0.3s;
}

.sidebar a:hover,
.sidebar a.active,
.sidebar router-link:hover,
.sidebar router-link.active {
  background-color: #fff2f2;
  color: #66A8EE;
}

.mdi {
  margin-right: 10px;
  font-size: 24px;
}

.logo {
  font-size: 24px;
  font-weight: bold;
  color: #66A8EE;
  text-align: center;
  margin-bottom: 30px;
}

.login-container {
  margin-top: auto;
  padding: 15px 20px;
  background-color: #ffffff;
  border-top: 1px solid #e8e8e8;
  width: 100%;
}

.user-info {
  display: flex;
  align-items: center;
  justify-content: center;
  color: #333;
  font-weight: 500;
}

/* 深色模式 */
@media (prefers-color-scheme: dark) {
  .sidebar {
    background-color: #1a1a1a;
    border-right: 1px solid #333;
  }
}

.login-button-wrapper {
  margin: 20px 0;
}

.login-button-wrapper :deep(.login-container) {
  padding: 10px;
}
</style>
