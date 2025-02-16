<template>
    <div class="main-layout">
      <SideBar 
        @openAddEssay="openAddEssayModal"
        @openSubscribe="openSubscriptionModal"
      />
      <div class="main-content">
        <TopBar />
        <InnerTopBar />
        <!-- 将 ContentArea 替换为 router-view -->
        <router-view v-slot="{ Component }">
          <component :is="Component" :key="$route.fullPath" />
        </router-view>
      </div>
      <AddEssayModal 
        v-if="showAddEssayModal" 
        @close="closeAddEssayModal" 
        @essay-published="handleEssayPublished" 
      />
      <SubscriptionModal
        v-model="showSubscriptionModal"
      />
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import SideBar from '@/components/layout/SideBar.vue'
  import TopBar from '@/components/layout/TopBar.vue'
  import AddEssayModal from '@/views/essay/AddEssayModal.vue'
  import SubscriptionModal from '@/components/layout/SubscriptionModal.vue'
  
  const router = useRouter()
  const showAddEssayModal = ref(false)
  const showSubscriptionModal = ref(false)
  
  const openAddEssayModal = () => {
    showAddEssayModal.value = true
  }
  
  const closeAddEssayModal = () => {
    showAddEssayModal.value = false
  }
  
  const openSubscriptionModal = () => {
    showSubscriptionModal.value = true
  }
  
  const handleEssayPublished = () => {
    closeAddEssayModal()
    // 刷新当前路由
    router.replace(router.currentRoute.value.fullPath)
  }
  </script>
  
  <style scoped>
  .main-layout {
    display: flex;
    min-height: 100vh;
    background-color: #FFFFFF;
    backdrop-filter: blur(10px);
    overflow: hidden; /* 防止整体出现滚动条 */
  }
  
  .main-content {
    flex-grow: 1;
    margin-left: 250px;
    display: flex;
    flex-direction: column;
    overflow-y: auto; /* 允许内容区域垂直滚动 */
    overflow-x: hidden; /* 禁止水平滚动 */
    height: 100vh; /* 确保内容区域占满视口高度 */
    border: none;
    padding-right: 24px; /* 添加右侧内边距 */
  }
  </style>