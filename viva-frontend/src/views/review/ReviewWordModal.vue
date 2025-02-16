<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <div class="content-wrapper">
        <div class="review-card" :key="currentWordIndex">
          <div class="context-section">
            <p v-html="highlightedContext"></p>
          </div>
          <div class="translation-section">
            <p>笔记: {{ currentWord.incorrect_translation }}</p>
          </div>
          <div class="input-section">
            <input 
              type="text" 
              v-model="userTranslation" 
              placeholder="输入正确的翻译"
              class="translation-input"
              :disabled="showAnswer"
              @keyup.enter="handleShowAnswer"
            />
            <div v-if="showAnswer" class="answer-section">
              <div class="correct-answer">
                正确答案: {{ currentWord.correct_translation }}
              </div>
              <div class="memory-buttons">
                <button 
                  v-for="level in memoryLevels" 
                  :key="level.value"
                  :class="['memory-button', level.class]"
                  @click="handleMemoryLevel(level.value)"
                >
                  {{ level.label }}
                  <span class="time-hint">{{ level.timeHint }}</span>
                </button>
              </div>
            </div>
            <div v-else class="action-section">
              <button class="show-answer-button" @click="handleShowAnswer">Show Answer</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue';
import api from '@/services/api';

const emit = defineEmits(['close']);

const wordReviewList = ref([]);
const currentWordIndex = ref(0);
const currentWord = ref({});
const userTranslation = ref('');
const showAnswer = ref(false);
const cardPosition = ref(0);

// Memory level definitions
const memoryLevels = [
  { label: 'Again', value: 0, timeHint: '<10m', class: 'again' },
  { label: 'Hard', value: 1, timeHint: '<15m', class: 'hard' },
  { label: 'Good', value: 2, timeHint: '1d', class: 'good' },
  { label: 'Easy', value: 3, timeHint: '2d', class: 'easy' }
];

// Mock data for word review list
const mockWordReviewList = [
  {
    id: 1,
    word: "推进",
    context: "配合年度目标（身体、知识、财务等）的稳步的推进，你对个人知识沉淀与项目复盘都在逐步形成高内聚的体系化内容。",
    incorrect_translation: "improvement",
    correct_translation: "advancement, promotion, propulsion",
    is_know: false
  },
  {
    id: 2,
    word: "paradigm",
    context: "This new teaching paradigm has completely transformed how we approach education in the digital age.",
    incorrect_translation: "模仿",
    correct_translation: "范例，模式，典范",
    is_know: false
  },
  {
    id: 3,
    word: "leverage",
    context: "We need to leverage our existing resources to maximize the project's impact.",
    incorrect_translation: "平衡",
    correct_translation: "利用，充分发挥",
    is_know: false
  }
];

const getWordReviewListData = async () => {
  try {
    wordReviewList.value = mockWordReviewList;
    if (wordReviewList.value.length > 0) {
      currentWord.value = wordReviewList.value[currentWordIndex.value];
    }
    return mockWordReviewList;
  } catch (error) {
    console.error('Error fetching word review list:', error);
  }
};

onMounted(() => {
  getWordReviewListData();
});

const handleShowAnswer = () => {
  if (userTranslation.value.trim() === '') {
    return;
  }
  showAnswer.value = true;
};

const answerStatus = computed(() => {
  if (!showAnswer.value) return '';
  return isAnswerCorrect.value ? 'correct' : 'incorrect';
});

const isAnswerCorrect = computed(() => {
  const correctAnswers = currentWord.value.correct_translation.split(/[,，]/).map(s => s.trim());
  return correctAnswers.includes(userTranslation.value.trim());
});

const cardStyle = computed(() => ({
  transform: `translateX(${cardPosition.value}px)`,
  transition: 'transform 0.3s ease-out'
}));

const handleMemoryLevel = async (level) => {
  // Here you would typically send the level to your backend
  console.log(`Memory level selected: ${level}`);
  
  // Animate card sliding out
  cardPosition.value = window.innerWidth;
  
  // Wait for animation to complete
  setTimeout(() => {
    // Move to next word
    if (currentWordIndex.value < wordReviewList.value.length - 1) {
      currentWordIndex.value++;
      currentWord.value = wordReviewList.value[currentWordIndex.value];
      // Reset states
      userTranslation.value = '';
      showAnswer.value = false;
      cardPosition.value = 0;
    } else {
      emit('close');
    }
  }, 300);
};

const highlightedContext = computed(() => {
  if (!currentWord.value?.context || !currentWord.value?.word) return '';
  
  const word = currentWord.value.word;
  const context = currentWord.value.context;
  
  return context.replace(
    new RegExp(word, 'g'), 
    `<span class="highlight">${word}</span>`
  );
});
</script>

<style scoped>
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
  background-color: var(--color-bg-white);
  width: 90%;
  max-width: 800px;
  border-radius: 20px;
  overflow: hidden;
  position: relative;
  padding: 20px;
}

.content-wrapper {
  position: relative;
  display: flex;
  flex-direction: column;
  width: 100%;
  align-items: center;
}

.review-card {
  background-color: var(--color-bg-white);
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  width: 100%;
  min-height: 400px;
  display: flex;
  flex-direction: column;
}

.context-section {
  background-color: #f8f9fa;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 16px;
  font-size: 16px;
  line-height: 1.6;
}

.translation-section {
  background-color: #eff6ff;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 16px;
}

.input-section {
  display: flex;
  flex-direction: column;
  flex: 1;
  position: relative;
}

.translation-input {
  width: 100%;
  padding: 12px;
  border: 1px solid #dcdfe6;
  border-radius: 8px;
  font-size: 16px;
  background-color: white;
  margin-bottom: 16px;
}

.action-section {
  margin-top: auto;
  padding: 20px 0;
}

.answer-section {
  margin-top: auto;
  padding: 20px 0;
}

.show-answer-button {
  width: 100%;
  background-color: var(--color-button-dark);
  color: white;
  border: none;
  padding: 12px;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.correct-answer {
  background-color: rgba(76, 175, 80, 0.1);
  color: #4CAF50;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 16px;
}

.memory-buttons {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  background-color: transparent;
  padding: 16px;
  border-radius: 8px;
}

.memory-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 12px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 500;
  background-color: var(--color-bg-white);
}

.memory-button .time-hint {
  font-size: 0.8rem;
  opacity: 0.7;
  margin-top: 4px;
}

.memory-button.again {
  color: #ef5350;
  border-color: #ef5350;
}

.memory-button.hard {
  color: #FFC107;
  border-color: #FFC107;
}

.memory-button.good {
  color: #4CAF50;
  border-color: #4CAF50;
}

.memory-button.easy {
  color: #2196F3;
  border-color: #2196F3;
}

.memory-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.memory-button.again:hover {
  background-color: #fff5f5;
}

.memory-button.hard:hover {
  background-color: #fffbeb;
}

.memory-button.good:hover {
  background-color: #f0fdf4;
}

.memory-button.easy:hover {
  background-color: #f0f9ff;
}

.highlight {
  background-color: #e6f4ff;
  color: #1890ff;
  padding: 2px 4px;
  border-radius: 4px;
  font-weight: 500;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
  padding: 5px;
  z-index: 1;
}

/* Dark mode styles */
@media (prefers-color-scheme: dark) {
  .modal-content {
    background-color: var(--color-bg-white);
  }

  .review-card {
    background-color: var(--color-bg-white);
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  }

  .context-section {
    background-color: #f8f9fa;
    color: var(--color-text-primary);
  }

  .translation-section {
    background-color: #eff6ff;
    color: var(--color-text-primary);
  }

  .translation-input {
    background-color: #2c2c2e;
    border-color: #4a4a4a;
    color: white;
  }

  .correct-answer {
    background-color: rgba(76, 175, 80, 0.2);
  }

  .highlight {
    background-color: rgba(24, 144, 255, 0.15);
    color: #40a9ff;
  }

  .close-button {
    color: #999;
  }

  .memory-buttons {
    background-color: transparent;
  }

  .memory-button {
    background-color: var(--color-bg-white);
    border-color: #e0e0e0;
    color: var(--color-text-primary);
  }

  .memory-button .time-hint {
    color: var(--color-text-secondary);
  }

  .memory-button:hover {
    box-shadow: 0 2px 8px rgba(255, 255, 255, 0.1);
  }

  .memory-button.again {
    color: #ef5350;
    border-color: #ef5350;
  }

  .memory-button.hard {
    color: #FFC107;
    border-color: #FFC107;
  }

  .memory-button.good {
    color: #4CAF50;
    border-color: #4CAF50;
  }

  .memory-button.easy {
    color: #2196F3;
    border-color: #2196F3;
  }

  .memory-button.again:hover {
    background-color: rgba(239, 83, 80, 0.1);
  }

  .memory-button.hard:hover {
    background-color: rgba(255, 193, 7, 0.1);
  }

  .memory-button.good:hover {
    background-color: rgba(76, 175, 80, 0.1);
  }

  .memory-button.easy:hover {
    background-color: rgba(33, 150, 243, 0.1);
  }
}

/* Mobile responsive styles */
@media (max-width: 768px) {
  .memory-buttons {
    grid-template-columns: repeat(2, 1fr);
  }

  .modal-content {
    width: 95%;
    padding: 15px;
  }
}
</style>
