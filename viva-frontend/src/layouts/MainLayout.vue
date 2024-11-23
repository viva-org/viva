<template>
    <div class="main-layout">
      <SideBar @openAddEssay="openAddEssayModal" />
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
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import SideBar from '@/components/layout/SideBar.vue'
  import TopBar from '@/components/layout/TopBar.vue'
  import InnerTopBar from '@/components/layout/InnerTopBar.vue'
  import AddEssayModal from '@/views/essay/AddEssayModal.vue'
  
  const router = useRouter()
  const showAddEssayModal = ref(false)
  
  const openAddEssayModal = () => {
    showAddEssayModal.value = true
  }
  
  const closeAddEssayModal = () => {
    showAddEssayModal.value = false
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
  }
  
  .main-content {
    flex-grow: 1;
    margin-left: 280px;
    display: flex;
    flex-direction: column;
  }
  </style>