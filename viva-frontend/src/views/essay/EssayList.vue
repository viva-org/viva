<template>
  <ContentArea>
    <div class="essay-list">
      <div class="essay-grid">
        <div v-for="essay in essays" :key="essay.essay_id" class="essay-card" @click="openEssay(essay)">
          <!-- Image Section -->
          <div class="essay-image-container">
            <img :src="essay.image_url" :alt="essay.title" class="essay-image">
          </div>
          
          <!-- Content Section -->
          <div class="essay-content">
            <div class="essay-header">
              <h3 class="essay-title">{{ essay.title }}</h3>
              <button class="more-options">
                <i class="el-icon-more"></i>
              </button>
            </div>
            <p class="essay-description">{{ truncateContent(essay.content) }}</p>
          </div>
          
          <!-- Footer Section -->
          <div class="essay-footer">
            <div class="essay-stats">
              <span class="word-count">{{ getWordCount(essay.content) }} words</span>
              <span class="update-time">{{ formatDate(essay.update_time) }}</span>
            </div>
          </div>
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

const truncateContent = (content) => {
  return content.length > 100 ? content.slice(0, 100) + '...' : content;
};

const getWordCount = (content) => {
  return content.split(/\s+/).length;
};

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString();
};

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
  padding: 24px;
  width: 100%;
  max-width: 1400px; /* 限制最大宽度 */
  margin: 0 auto; /* 居中显示 */
  box-sizing: border-box;
}

.essay-grid {
  display: grid;
  width: 100%;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 24px;
  box-sizing: border-box;
}

/* 调整不同屏幕宽度下的列数 */
@media (min-width: 1400px) {
  .essay-grid {
    grid-template-columns: repeat(5, 1fr); /* 大屏幕显示5列 */
  }
}

@media (max-width: 1399px) and (min-width: 1100px) {
  .essay-grid {
    grid-template-columns: repeat(4, 1fr); /* 中等屏幕显示4列 */
  }
}

@media (max-width: 1099px) and (min-width: 800px) {
  .essay-grid {
    grid-template-columns: repeat(3, 1fr); /* 小屏幕显示3列 */
  }
}

@media (max-width: 799px) and (min-width: 500px) {
  .essay-grid {
    grid-template-columns: repeat(2, 1fr); /* 更小屏幕显示2列 */
  }
}

@media (max-width: 499px) {
  .essay-grid {
    grid-template-columns: 1fr; /* 手机屏幕显示1列 */
  }
  
  .essay-list {
    padding: 16px;
  }
}

.essay-card {
  position: relative;
  width: 100%;
  min-height: 200px;
  height: 320px;
  display: flex;
  flex-direction: column;
  font-family: inherit;
  font-size: 100%;
  font-style: inherit;
  font-variant: inherit;
  font-weight: inherit;
  margin: 0;
  padding: 0;
  vertical-align: baseline;
  border-radius: 8px;
  border: 1px solid rgb(218, 220, 224);
  overflow: hidden;
  box-sizing: border-box;
  background-color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.essay-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.2);
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: 1;
  pointer-events: none;
}

.essay-card:hover {
  transform: translateY(-2px);
}

.essay-card:hover::before {
  opacity: 1;
}

.essay-image-container {
  position: relative;
  height: 180px;
  overflow: hidden;
  background-color: #f5f5f5;
}

.essay-image-container::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, 
    rgba(0, 0, 0, 0) 0%,
    rgba(0, 0, 0, 0) 50%,
    rgba(0, 0, 0, 0.02) 100%
  );
  opacity: 0;
  transition: opacity 0.3s ease;
}

.essay-card:hover .essay-image-container::after {
  opacity: 1;
}

.essay-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.essay-content {
  position: relative;
  flex: 1;
  min-height: 140px;
  padding-top: 26px;
  padding-bottom: 26px;
  padding-left: 10px;
  padding-right: 10px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  background-color: white;
  z-index: 2;
}

.essay-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 4px;
}

.essay-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #202124;
  line-height: 1.3;
}

.more-options {
  position: relative;
  z-index: 3;
  opacity: 0;
  transition: opacity 0.3s ease;
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  color: #fff;
}

.essay-card:hover .more-options {
  opacity: 1;
}

.essay-description {
  margin: 0;
  font-size: 14px;
  color: #5f6368;
  line-height: 1.4;
  flex: 1;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.essay-footer {
  position: relative;
  height: 40px;
  padding: 0 16px;
  border-top: 1px solid rgb(218, 220, 224);
  background-color: #fff;
  display: flex;
  align-items: center;
  z-index: 2;
}

.essay-stats {
  display: flex;
  justify-content: space-between;
  width: 100%;
  font-size: 13px;
  color: #5f6368;
}

.word-count, .update-time {
  display: flex;
  align-items: center;
  gap: 4px;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .essay-card {
    background-color: #2d2d2d;
    border-color: rgba(255, 255, 255, 0.1);
  }

  .essay-content {
    background-color: #2d2d2d;
  }

  .essay-title {
    color: #fff;
  }

  .essay-description {
    color: rgba(255, 255, 255, 0.7);
  }

  .essay-footer {
    background-color: #262626;
    border-top-color: rgba(255, 255, 255, 0.1);
  }

  .essay-stats {
    color: rgba(255, 255, 255, 0.7);
  }

  .essay-card::before {
    background: rgba(0, 0, 0, 0.4);
  }
  
  .essay-card:hover .essay-content,
  .essay-card:hover .essay-footer {
    background-color: rgba(45, 45, 45, 0.7);
  }
}
</style>
