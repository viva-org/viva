<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <button class="close-button" @click="$emit('close')">×</button>
      <div v-if="!isPracticing" class="essay-content">
        <h2>{{ essay.title }}</h2>
        <img :src="essay.image" alt="Essay Image" class="detail-image" />
        <p>{{ essay.content }}</p>
        <button class="start-practice-button" @click="startPractice">开始练习</button>
      </div>
      <div v-else class="practice-content">
        <div class="content-wrapper">
          <div class="page-button left" @click="prevSentence" v-show="currentSentenceIndex > 0" :class="{ 'button-disabled': currentSentenceIndex === 0 }">
            <el-icon><ArrowLeft /></el-icon>
          </div>
          <div class="sentence-container">
            <SentenceCard 
            v-if="currentSentence" 
            :sentenceData="currentSentence"
            :show-results="currentShowResults"
            />
          </div>

          <div class="page-button right" @click="nextSentence" v-show="currentSentenceIndex < sentenceIds.length - 1" :class="{ 'button-disabled': currentSentenceIndex === sentenceIds.length - 1 }">
            <el-icon><ArrowRight /></el-icon>
          </div>
          <div class="bottom-controls">
            <div class="check-button-container">
              <el-button
                class="check-button"
                type="primary"
                circle
                @click="handleCheckCurrentSentence"
                :loading="checkAllLoading"
              >
                <el-icon><Check /></el-icon>
              </el-button>
            </div>

            <div class="pagination-container">
              <div class="pagination-info">
                {{ currentSentenceIndex + 1 }} / {{ sentenceIds.length }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import api from '@/services/api';
import SentenceCard from '@/components/essay/SentenceCard.vue';
import { ArrowLeft, ArrowRight, Check } from '@element-plus/icons-vue';

const props = defineProps({
  essay: {
    type: Object,
    required: true
  }
});
// 使用数组而不是 Map 来存储状态
const showResultsArray = ref([]);

const emit = defineEmits(['close']);

const sentenceIds = ref([]);
const currentSentenceIndex = ref(0);
const isPracticing = ref(false);
const currentSentence = ref(null);

const startPractice = async () => {
  try {
    const response = await api.getEssaySentenceIds(props.essay.essay_id);
    sentenceIds.value = response.data;
    if (sentenceIds.value.length > 0) {
      await fetchSentenceWithMappings(sentenceIds.value[0]);
    }
    isPracticing.value = true;
  } catch (error) {
    console.error('Error starting practice:', error);
  }
};

const fetchSentenceWithMappings = async (sentenceId) => {
  try {
    const response = await api.getSentenceWithMappings(sentenceId);
    currentSentence.value = response.data;
  } catch (error) {
    console.error('Error fetching sentence with mappings:', error);
  }
};

const nextSentence = async () => {
  if (currentSentenceIndex.value < sentenceIds.value.length - 1) {
    currentSentenceIndex.value++;
    await fetchSentenceWithMappings(sentenceIds.value[currentSentenceIndex.value]);
  }
};

const prevSentence = async () => {
  if (currentSentenceIndex.value > 0) {
    currentSentenceIndex.value--;
    await fetchSentenceWithMappings(sentenceIds.value[currentSentenceIndex.value]);
  }
};

// 获取当前句子的检查状态
const currentShowResults = computed(() => 
    showResultsArray.value[currentSentenceIndex.value] || false
);

// 处理检查状态的方法
const handleCheckCurrentSentence = () => {
    console.log("爷组件处理前", currentShowResults.value);
    
    // 直接设置当前索引的状态为 true
    showResultsArray.value[currentSentenceIndex.value] = true;
    
    console.log("更新后的状态:", {
        index: currentSentenceIndex.value,
        value: showResultsArray.value[currentSentenceIndex.value]
    });
};
</script>

<style scoped>
.modal-overlay {
  display: flex;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.modal-content {
  background-color: #ffffff;
  width: 90%;
  max-width: 800px;
  height: 90vh;
  border-radius: 20px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  position: relative;
}

.close-button {
  position: absolute;
  top: 16px;
  right: 16px;
  font-size: 24px;
  background: none;
  border: none;
  cursor: pointer;
  color: #333333;
}

.essay-content {
  flex: 1;
  overflow-y: hidden; /* 允许内容垂直滚动 */
  padding: 24px;
  display: flex;
  flex-direction: column;
  align-items: stretch;
}

.essay-content h2 {
  font-size: 28px;
  color: #333333;
  margin: 0 0 16px;
}

.detail-image {
  width: 100%;
  max-height: 300px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 16px;
}

.essay-content p {
  background-color: #f8f9fa;
  padding: 16px;
  border-radius: 8px;
  font-size: 16px;
  line-height: 1.6;
  color: #495057;
  overflow-wrap: break-word; /* 确保长单词也能换行 */
}

.start-practice-button {
  align-self: center;
  padding: 12px 24px;
  background-color: var(--color-primary);
  color: #ffffff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  transition: background-color 0.3s ease;
  margin-top: 20px;
  margin-bottom: 20px; /* 添加底部边距 */
}
.page-control-bar {
  display: flex;
  gap: 16px;
  background-color: rgba(255, 255, 255, 0.9);
  padding: 8px 16px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  pointer-events: auto; /* 恢复控制栏的点击事件 */
}

.control-section {
  display: flex;
  align-items: center;
}

.control-section:not(:last-child) {
  border-right: 1px solid rgba(0, 0, 0, 0.1);
  padding-right: 16px;
}

.control-section:not(:first-child) {
  padding-left: 16px;
}

.page-control-bar :deep(.el-button) {
  margin: 0;
  height: 32px;
  font-size: 14px;
}

.pagination-info {
  padding: 6px 12px;
  background-color: rgba(0, 0, 0, 0.04);
  border-radius: 8px;
  font-size: 14px;
  color: #606266;
  min-width: 60px;
  text-align: center;
}

/* 深色模式支持 */
@media (prefers-color-scheme: dark) {
  .page-control-bar {
    background-color: rgba(40, 40, 40, 0.9);
    border-color: rgba(255, 255, 255, 0.1);
  }

  .pagination-info {
    background-color: rgba(255, 255, 255, 0.08);
    color: #e0e0e0;
  }
}

/* 移动端适配 */
@media (max-width: 768px) {
  .page-control-bar {
    padding: 6px 12px;
    gap: 8px;
  }

  .pagination-info {
    padding: 4px 8px;
    font-size: 13px;
  }
}
.start-practice-button:hover {
  background-color: #1CA5E3;
}

.practice-content {
  position: relative;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.content-wrapper {
  position: relative;
  display: flex;
  flex: 1;
  overflow: hidden;
  padding: 24px 64px;
  background-color: #f8f8f8;
}

.sentence-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: #FAFBFC;
  border-radius: 20px;
  box-shadow:
    0 4px 6px rgba(0, 0, 0, 0.02),
    0 10px 20px rgba(37, 99, 235, 0.05);
  overflow: hidden;
  margin: 0 auto;
  max-width: 680px;
  border: 1px solid rgba(226, 232, 240, 0.8);
  transition: all 0.3s ease;
}

.pagination-info {
  padding: 10px;
  background-color: #f0f0f0;
  text-align: center;
  border-top: 1px solid #ddd;
  font-size: 14px;
}

.page-button {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 40px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(255, 255, 255, 0.5);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.page-button:hover {
  background-color: rgba(255, 255, 255, 0.95);
  transform: translateY(-50%) scale(1.02);
}

.page-button.left { left: 16px; }
.page-button.right { right: 16px; }

.page-button :deep(.el-icon) {
  font-size: 20px;
  color: #1d1d1f;
}

.bottom-controls {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 80px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
  background: linear-gradient(to bottom, transparent, rgba(248, 248, 248, 0.95) 40%);
}

.check-button {
  width: 50px !important;
  height: 50px !important;
  font-size: 22px !important;
  background-color: #007AFF !important;
  border: none !important;
  box-shadow: 0 4px 12px rgba(0, 122, 255, 0.3);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.check-button:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 16px rgba(0, 122, 255, 0.4);
}

.check-button:active {
  transform: scale(0.95);
}

.pagination-container {
  position: absolute;
  bottom: 24px;
  right: 24px;
  z-index: 20;
}

.pagination-info {
  background-color: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  padding: 8px 16px;
  border-radius: 15px;
  font-size: 14px;
  color: #1d1d1f;
  font-weight: 500;
  letter-spacing: 0.5px;
}

/* 深色模式 */
@media (prefers-color-scheme: dark) {
  .content-wrapper {
    background-color: #1c1c1e;
  }

  .sentence-container {
    background-color: #1A1C1E;
    border-color: rgba(255, 255, 255, 0.1);
    box-shadow: 
      0 4px 6px rgba(0, 0, 0, 0.1),
      0 10px 20px rgba(0, 0, 0, 0.15);
  }

  .page-button {
    background-color: rgba(50, 50, 50, 0.9);
  }

  .page-button:hover {
    background-color: rgba(60, 60, 60, 0.95);
  }

  .page-button :deep(.el-icon) {
    color: #ffffff;
  }

  .bottom-controls {
    background: linear-gradient(to bottom, transparent, rgba(28, 28, 30, 0.95) 40%);
  }

  .pagination-info {
    background-color: rgba(50, 50, 50, 0.9);
    color: #ffffff;
  }
}

/* 移动端适配 */
@media (max-width: 768px) {
  .content-wrapper {
    padding: 16px 48px;
  }

  .page-button {
    width: 36px;
    height: 72px;
  }

  .bottom-controls {
    height: 70px;
    padding: 0 16px;
  }

  .check-button {
    width: 44px !important;
    height: 44px !important;
    font-size: 20px !important;
  }

  .pagination-info {
    padding: 6px 12px;
    font-size: 13px;
  }
}
</style>
