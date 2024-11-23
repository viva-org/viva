<template>
  <ContentArea>
    <div class="essay-list">
      <div
        class="essay-card"
        v-for="essay in essays"
        :key="essay.essay_id"
        @click="openEssay(essay)"
      >
        <img
          :src="essay.image_url || defaultImageUrl"
          alt="Essay Image"
          class="essay-image"
        />
        <div class="essay-content">
          <h3 class="essay-title">{{ essay.title }}</h3>
          <p class="essay-excerpt">{{ getExcerpt(essay.content) }}</p>
        </div>
      </div>

      <EssayDetailModal
        v-if="selectedEssay"
        :essay="selectedEssay"
        @close="closeEssay"
      />
    </div>
  </ContentArea>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import api from '@/services/api'
import EssayDetailModal from '@/views/essay/EssayDetailModal.vue'
import ContentArea from '@/components/layout/ContentArea.vue'

const route = useRoute()
const essays = ref([])
const defaultImageUrl = ref('https://imagehosting4picgo.oss-cn-beijing.aliyuncs.com/imagehosting/fix-dir%2Fpicgo%2Fpicgo-clipboard-images%2F2024%2F10%2F13%2F14-17-55-7799d9267d2f77470aa05c174755f27e-202410131417361-105db7.png') // 添加默认图片URL

const fetchEssays = async () => {
  try {
    const response = await api.getEssays()
    essays.value = response.data
  } catch (error) {
    console.error('获取文章列表错误:', error)
  }
}

const getExcerpt = (content) => {
  return content.length > 100 ? content.slice(0, 100) + '...' : content
}

const openEssay = (essay) => {
  selectedEssay.value = essay
}

const closeEssay = () => {
  selectedEssay.value = null
}

const selectedEssay = ref(null)

onMounted(() => {
  fetchEssays()
})

// 监听路由变化，重新获取文章列表
watch(() => route.fullPath, fetchEssays)
</script>

<style scoped>
.app-container {
  display: flex;
  min-height: 100vh;
  background-color: #f4f4f4;
}

.main-content {
  flex-grow: 1;
  margin-left: 280px;
  padding: 20px;
}

.essay-list {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 15px;
  padding: 15px;
}

/* 模态框样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: transparent; /* 改为透明 */
  width: 90%; /* 调整宽度 */
  max-width: 800px; /* 添加最大宽度 */
  height: 90vh; /* 设置高度 */
  max-height: 90vh; /* 设置最大高度 */
  overflow: hidden; /* 改为 hidden */
  border-radius: 8px;
  padding: 0; /* 移除内边距 */
}

/* 让背景在模态框出现时不能滚动 */
body.modal-open {
  overflow: hidden;
}

/* 添加过渡动画 */
.fade-enter-active, .fade-leave-active {
  transition: opacity .3s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

@media (max-width: 1600px) {
  .essay-list {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (max-width: 1200px) {
  .essay-list {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 992px) {
  .main-content {
    margin-left: 80px;
  }
  .essay-list {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
  }
  .essay-list {
    grid-template-columns: 1fr;
  }
}

.essay-card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: transform 0.3s ease;
}

.essay-card:hover {
  transform: translateY(-5px);
}

.essay-image {
  width: 100%;
  height: 150px;
  object-fit: cover;
}

.essay-content {
  padding: 10px;
}

.essay-title {
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 5px;
  line-height: 1.2;
}

.essay-excerpt {
  font-size: 12px;
  color: #666;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
