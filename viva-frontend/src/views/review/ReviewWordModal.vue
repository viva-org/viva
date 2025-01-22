<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <button class="close-button" @click="$emit('close')">×</button>
      <div class="practice-content">
        <div class="content-wrapper">
          <div class="page-button left" @click="prevWord" v-show="currentWordIndex > 0"
               :class="{ 'button-disabled': currentWordIndex === 0 }">
            <el-icon>
              <ArrowLeft/>
            </el-icon>
          </div>
          <div class="sentence-container">
            <p><strong>单词:</strong> {{ currentWord.word }}</p>
            <p><strong>释义:</strong> {{ currentWord.translation }}</p>
            <p><strong>例句:</strong> {{ currentWord.example_sentence }}</p>
          </div>
          <div class="rating">
            <label v-for="(level, index) in ratingLevels" :key="index">
              <input type="radio" v-model="selectedLevel" :value="level.value"/>
              {{ level.label }}
            </label>
          </div>
          <button @click="submitRating">提交掌握程度</button>
          <button v-if="!currentWord.is_know" @click="setKnow">标记熟知</button>
          <div class="page-button right" @click="nextWord" v-show="currentWordIndex < wordReviewList.length - 1"
               :class="{ 'button-disabled': currentWordIndex === wordReviewList.length - 1 }">
            <el-icon>
              <ArrowRight/>
            </el-icon>
          </div>
          <div class="bottom-controls">
            <div class="pagination-container">
              <div class="pagination-info">
                {{ currentWordIndex + 1 }} / {{ wordReviewList.length }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {onMounted, ref} from 'vue';
import api from '@/services/api';
import {ArrowLeft, ArrowRight} from '@element-plus/icons-vue';
import {ElMessageBox} from "element-plus";

const emit = defineEmits(['close']);

const wordReviewList = ref([]);
const currentWordIndex = ref(0);
const currentWord = ref({});
const selectedLevel = ref(null);


const ratingLevels = [
  {label: '完全不认识', value: 0},
  {label: '略有印象', value: 1},
  {label: '基本了解', value: 2},
  {label: '较为熟悉', value: 3},
  {label: '非常熟悉', value: 4},
  {label: '完全掌握', value: 5},
];

const getWordReviewListData = async () => {
  try {
    const response = await api.getWordReviewList()
    const data = response.data;
    if (data.status !== 0) {
      throw new Error('Failed to fetch word review list');
    }
    console.log('wordReviewList:', data.data)
    wordReviewList.value = data.data
    // 初始化 currentWord
    if (wordReviewList.value.length > 0) {
      currentWord.value = wordReviewList.value[currentWordIndex.value];
    } else {
      console.log('wordReviewList is empty');
      ElMessageBox.alert('今日没有单词要复习', '提示', {
        confirmButtonText: '确定',
        callback: () => {
          emit('close');
        }
      });
    }
    return data.data;
  } catch (error) {
    console.error('Error fetching word review list:', error);
  }
};

onMounted(() => {
  console.log("open ReviewWordModal")
  getWordReviewListData()
})

const nextWord = async () => {
  if (currentWordIndex.value < wordReviewList.value.length - 1) {
    currentWordIndex.value++;
    currentWord.value = wordReviewList.value[currentWordIndex.value]
  }
};

const prevWord = async () => {
  if (currentWordIndex.value > 0) {
    currentWordIndex.value--;
    currentWord.value = wordReviewList.value[currentWordIndex.value]
  }
};

const submitRating = () => {
  if (selectedLevel.value !== null) {
    console.log(`单词 "${currentWord.value.word}" 的掌握程度为 ${selectedLevel.value}`);
    updateWordReview(currentWord.value.id, selectedLevel.value)
    nextWord(); // 自动跳转到下一个单词
  } else {
    alert('请选择掌握程度');
  }
};

const setKnow = () => {
  console.log(`单词 "${currentWord.value.word}" 的is_know为 ${currentWord.value.is_know}`);
  updateWordReviewKnow(currentWord.value.id, !currentWord.value.is_know)
  nextWord(); // 自动跳转到下一个单词
};

const updateWordReview = async (id, quality) => {
  try {
    const response = await api.putWordReview(id, quality);
    const data = response.data;
    console.log(data);
    if (data.status !== 0) {
      throw new Error('Failed to update word');
    }
    return data.data;
  } catch (error) {
    console.error('Error fetching word stats:', error);
  }
};

const updateWordReviewKnow = async (id, is_know) => {
  try {
    const response = await api.postWordReviewKnow(id, is_know);
    const data = response.data;
    console.log(data);
    if (data.status !== 0) {
      throw new Error('Failed to update word');
    }
    return data.data;
  } catch (error) {
    console.error('Error fetching word stats:', error);
  }
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(252, 252, 252, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
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
  box-shadow: 0 8px 30px rgba(42, 161, 240, 0.263);
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

.essay-content h2 {
  font-size: 28px;
  color: #333333;
  margin: 0 0 16px;
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

  .pagination-info {
    background-color: rgba(255, 255, 255, 0.08);
    color: #e0e0e0;
  }
}

/* 移动端适配 */
@media (max-width: 768px) {
  .pagination-info {
    padding: 4px 8px;
    font-size: 13px;
  }
}

.practice-content {
  flex: 1;
  padding: 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.content-wrapper {
  position: relative;
  display: flex;
  flex-direction: column;
  width: 100%;
  align-items: center;
}

.sentence-container {
  flex: 1;
  flex-direction: column;
  background-color: #FAFBFC;
  border-radius: 20px;
  margin: 0 auto;
  min-width: 600px;
  min-height: 500px;
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

.page-button.left {
  left: 16px;
}

.page-button.right {
  right: 16px;
}

.page-button :deep(.el-icon) {
  font-size: 20px;
  color: #1d1d1f;
}

.bottom-controls {
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
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1),
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


  .pagination-info {
    padding: 6px 12px;
    font-size: 13px;
  }
}
</style>
