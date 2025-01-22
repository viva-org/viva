<template>

    <div class="mapping-input-grid">
      <div
        v-for="(mapping, index) in mappings"
        :key="index"
        class="mapping-input-item"
        :class="{
          'hover-border': !props.showResults,
        }"
      >
        <div
          class="mapping-card"
          :class="{
            'is-flipped': flippedStates[index],
            'correct': props.showResults && !mapping.isAddedToAnki && isExactMatch(inputs[mapping.focus_word], mapping.ai_review.ai_review_expression),
            'partially-correct': props.showResults && !mapping.isAddedToAnki && isPartialMatch(inputs[mapping.focus_word], mapping.ai_review.ai_review_expression),
            'incorrect': props.showResults && !mapping.isAddedToAnki && isIncorrect(inputs[mapping.focus_word], mapping.ai_review.ai_review_expression),
            'flippable': props.showResults && !mapping.isAddedToAnki,
            'added-to-anki-front': mapping.isAddedToAnki,
            'reset-background': mapping.isAddedToAnki
          }"
          @mouseenter="props.showResults && !mapping.isAddedToAnki && hoverCard(index)"
          @mouseleave="props.showResults && !mapping.isAddedToAnki && leaveCard(index)"
        >
          <!-- 卡片正面 -->
          <div class="mapping-card-front card-face">
            <!-- 要翻译的中文单词 -->
            <label :for="`mapping-input-${index}`" class="mapping-label">{{ mapping.focus_word }}</label>
            <!-- 输入框 -->
            <input
              :id="`mapping-input-${index}`"
              :ref="el => { if (el) inputRefs[index] = el }"
              :value="inputs[mapping.focus_word] || ''"
              @input="updateInput(mapping.focus_word, $event.target.value)"
              @keydown.enter.prevent="handleEnterKey(index)"
              @focus="handleFocus(mapping.focus_word)"
              @blur="handleBlur"
              :class="{ 
                'active-input': activeIndex === index,
                'no-translation': !mapping.is_need_translation 
              }"
              class="mapping-input"
              :disabled="!mapping.is_need_translation"
            />

            <!-- 显示 AI 检查不通过的错误信息 -->
            <div v-if="props.showResults" class="error-message">
               {{ mapping.ai_review.ai_review_expression.replace(/[{}]/g, '') }}
            </div>
          </div>
          
          <!-- 卡片背面 -->
          <div class="mapping-card-back card-face">
            <button @click="handleAddToAnki(mapping, index)" :disabled="mapping.isAddedToAnki" class="mapping-button">
              {{ mapping.isAddedToAnki ? '已添加到Anki' : '加入Anki' }}
            </button>
            <button @click="handleAddToReview(mapping, index)" :disabled="mapping.isAddedToReview" class="mapping-button">
              {{ mapping.isAddedToReview ? '已添加到单词本' : '加入单词本' }}
            </button>
          </div>
        </div>
      </div>
  </div>
</template>

<script setup>
import {computed, inject, ref, watch} from 'vue'

// Props 定义
const props = defineProps({
  mappings: {
    type: Array,
    required: true
  },
  checkAllLoading: {
    type: Boolean,
    default: false
  },
  showResults: {
    type: Boolean,
    default: false
  } 
});

// Emits 定义
const emit = defineEmits([
  'update-input', 
  'enter-pressed', 
  'focus', 
  'add-to-anki', 
  'add-to-review',
  'update-mapping'
]);

// Refs
const inputRefs = ref({});
const activeIndex = ref(-1);
const flippedStates = ref({});


// Injections
const inputs = inject('inputs', ref({}));
const focusedWord = inject('focusedWord');
const addedToAnkiWords = inject('addedToAnkiWords');

// Methods
const updateInput = (focusWord, value) => {
  if (inputs) {
    inputs[focusWord] = value;
  }
  emit('update-input', focusWord, value);
};

const handleEnterKey = (index) => {
  emit('enter-pressed', index);
};

const handleFocus = (focusWord) => {
  focusedWord.value = focusWord;
  console.log(focusedWord.value);
  emit('focus', focusWord);
};

const handleBlur = () => {
  focusedWord.value = '';
};

const hoverCard = (index) => {
  if (props.mappings[index].ai_review) {
    flippedStates.value[index] = true;
  }
};

const leaveCard = (index) => {
  if (props.mappings[index].ai_review) {
    flippedStates.value[index] = false;
  }
};

watch(() => props.showResults, (newValue) => {
  console.log("子组件 watch 到 showResults 变化:", newValue);
})



const computedMappings = computed({
  get: () => props.mappings,
  set: (newValue) => emit('update:mappings', newValue)
});

const isAddedToAnki = computed(() => {
  return (word) => addedToAnkiWords.value.has(word);
});

const handleAddToAnki = (mapping, index) => {
  console.log(mapping);
  emit('add-to-anki', mapping);
  // 添加成功后，确保卡片回到正面
  flippedStates.value[index] = false;
  // 更新mapping的状态
  mapping.isAddedToAnki = true;
};

const handleAddToReview = (mapping, index) => {
  console.log(mapping);
  emit('add-to-review', mapping);
  // 添加成功后，确保卡片回到正面
  flippedStates.value[index] = false;
  // 更新mapping的状态
  mapping.isAddedToReview = true;
};

// 添加一个辅助函数来处理答案字符串
const parseAnswers = (answersStr) => {
  if (!answersStr) return [];
  // 移除花括号并分割字符串
  return answersStr.replace(/[{}]/g, '').split(',').map(s => s.trim());
};

const isExactMatch = (input, aiReviewExpressions) => {
  const answers = parseAnswers(aiReviewExpressions);
  const trimmedInput = input?.trim()?.toLowerCase();
  
  console.log('isExactMatch check:', {
    input: trimmedInput,
    answers,
    firstAnswer: answers[0]
  });
  
  if (!answers.length || !trimmedInput) {
    console.log('Invalid input or empty answers, returning false');
    return false;
  }
  
  const result = trimmedInput === answers[0].toLowerCase().trim();
  console.log('Exact match result:', result);
  return result;
};

const isPartialMatch = (input, aiReviewExpressions) => {
  const answers = parseAnswers(aiReviewExpressions);
  const trimmedInput = input?.trim()?.toLowerCase();
  
  console.log('isPartialMatch check:', {
    input: trimmedInput,
    answers
  });
  
  if (!answers.length || !trimmedInput || answers.length <= 1) {
    console.log('Invalid input or not enough answers, returning false');
    return false;
  }
  
  const result = answers.slice(1).some(expr => 
    expr.toLowerCase().trim() === trimmedInput
  );
  
  console.log('Partial match result:', result);
  return result;
};

const isIncorrect = (input, aiReviewExpressions) => {
  const answers = parseAnswers(aiReviewExpressions);
  const trimmedInput = input?.trim()?.toLowerCase();
  
  console.log('isIncorrect check:', {
    input: trimmedInput,
    answers
  });
  
  if (!answers.length || !trimmedInput) {
    console.log('Invalid input or empty answers, returning true');
    return true;
  }
  
  const result = !answers.some(expr => 
    expr.toLowerCase().trim() === trimmedInput
  );
  
  console.log('Incorrect result:', result);
  return result;
};

// 添加一个 watch 来调试 inputs
watch(inputs, (newVal) => {
  console.log('inputs changed:', newVal);
}, { deep: true });
</script>

<style scoped>
.mapping-input-card {
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
  padding: 24px;
  margin-bottom: 32px;
  transition: box-shadow 0.3s ease;
}


.card-title {
  font-size: 20px;
  font-weight: 600;
  color: #1d1d1f;
}

.mapping-input-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); /* 调整最小宽度 */
  gap: 12px; /* 减小间距 */
}

.mapping-input-item {
  perspective: 1000px; /* 开启 3D 空间 */
  position: relative;
}

.mapping-input-item.hover-border:hover {
  border: 1px solid #dcdcdc; /* 悬停时的浅边框颜色 */
  border-radius: 8px;
  transition: border 0.2s;
}

.mapping-card {
  position: relative;
  width: 100%;
  height: 160px; /* 稍微减小卡片高度 */
  transform-style: preserve-3d;
  transition: transform 0.6s ease, background-color 0.3s ease;
}

.card-face {
  position: absolute;
  width: 100%;
  height: 100%; /* 使正反面高度一致 */
  backface-visibility: hidden;
  border-radius: 8px;
  padding: 10px;
  box-sizing: border-box;
}

.mapping-card-front {
  transform: rotateX(0deg);
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.mapping-card-back {
  transform: rotateX(180deg);
  background-color: #007aff;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  padding: 20px; /* 增加内边距 */
  border-radius: 8px; /* 圆角 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* 阴影效果 */
}

.correct .mapping-card-front {
  background-color: #e0ffe0; /* 浅绿色 */
}

.incorrect .mapping-card-front {
  background-color: #ffe0e0; /* 浅红色 */
}

.is-flipped {
  transform: rotateX(180deg);
}

.mapping-label {
  font-size: 15px;
  font-weight: 500;
  color: #1c1c1e;
  margin-bottom: 8px;
  text-align: center;
}

.mapping-input {
  font-size: 17px;
  padding: 10px 0;
  border: none;
  border-bottom: 1px solid #c6c6c8;
  background-color: transparent;
  color: #1c1c1e;
  transition: all 0.2s ease;
  text-align: center;
  width: 100%;
}

.mapping-input:focus {
  outline: none;
  border-bottom-color: #007aff;
}

.active-input {
  border-bottom-color: #007aff;
}

.no-translation {
  color: #8e8e93;
  border-bottom-color: #e5e5ea;
}

.error-message {
  color: #ff4d4f;
  margin-top: 5px;
  font-size: 14px;
  text-align: center;
  max-height: 40px;
  overflow: hidden;
}

.loading {
  opacity: 0.6;
  pointer-events: none;
}

.back-content {
  font-size: 16px;
  text-align: center;
}

/* 添加翻转效果 */
.flippable .mapping-card {
  cursor: pointer;
}

.flippable .mapping-card:hover {
  transform: rotateX(180deg);
}

/* 深色模式调整 */
@media (prefers-color-scheme: dark) {
  .mapping-input-card {
    background-color: #1c1c1e;
  }

  .mapping-input-card:hover {
    box-shadow: 0 4px 12px rgba(255, 255, 255, 0.1);
  }

  .card-title {
    color: #f5f5f7;
  }

  .mapping-label {
    color: #ffffff;
  }

  .mapping-input {
    color: #ffffff;
    border-bottom-color: #48484a;
  }

  .no-translation {
    color: #8e8e93;
    border-bottom-color: #3a3a3c;
  }

  .correct .mapping-card-front {
    background-color: #2ecc71; /* 深绿色 */
  }

  .incorrect .mapping-card-front {
    background-color: #e74c3c; /* 深红色 */
  }

  .mapping-card-back {
    background-color: #0a84ff;
  }

  .mapping-input-item.hover-border:hover {
    border-color: #3a3a3c;
  }
}

/* 覆盖上部25%的透明层 */
.top-third-overlay {
  position: absolute;
  top: 0;
  height: 25%;
  width: 100%;
  cursor: pointer;
  background-color: rgba(0, 0, 0, 0); /* 透明背景 */
}

/* 添加新的样式 */
.mapping-card-back {
    cursor: pointer;
}

.mapping-card-back .back-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

/* 已添加状态的样式 */
.mapping-card.added .mapping-card-back {
    background-color: #67c23a;
}

/* 禁用状态的样式 */
.mapping-card-back.disabled {
    background-color: #909399;
    cursor: not-allowed;
}

/* 添加到Anki后的正面样式 */
.added-to-anki-front {
  background-color: rgba(0, 122, 255, 0.1); /* 苹果系统淡蓝色 */
  transition: background-color 0.3s ease;
}

/* 禁用已添加到Anki的卡片的翻转效果 */
.added-to-anki-front.is-flipped {
  transform: rotateX(0deg) !important;
}

/* 可选：添加一个小图标或标记表示已添加状态 */
.added-to-anki-front .mapping-card-front::after {
  content: "✓";
  position: absolute;
  top: 8px;
  right: 8px;
  color: #34C759; /* 苹果系统绿色 */
  font-size: 14px;
}

/* 已添加状态下禁用hover效果 */
.added-to-anki-front:hover {
  transform: none;
  cursor: default;
}

/* 添加翻转效果 */
.flippable .mapping-card {
  cursor: pointer;
}

.flippable .mapping-card:hover {
  transform: rotateX(180deg);
}

/* 深色模式调整 */
@media (prefers-color-scheme: dark) {
  .mapping-input-card {
    background-color: #1c1c1e;
  }

  .mapping-input-card:hover {
    box-shadow: 0 4px 12px rgba(255, 255, 255, 0.1);
  }

  .card-title {
    color: #f5f5f7;
  }

  .mapping-label {
    color: #ffffff;
  }

  .mapping-input {
    color: #ffffff;
    border-bottom-color: #48484a;
  }

  .no-translation {
    color: #8e8e93;
    border-bottom-color: #3a3a3c;
  }

  .correct .mapping-card-front {
    background-color: #2ecc71; /* 深绿色 */
  }

  .incorrect .mapping-card-front {
    background-color: #e74c3c; /* 深红色 */
  }

  .mapping-card-back {
    background-color: #0a84ff;
  }

  .mapping-input-item.hover-border:hover {
    border-color: #3a3a3c;
  }
}

/* 覆盖上部25%的透明层 */
.top-third-overlay {
  position: absolute;
  top: 0;
  height: 25%;
  width: 100%;
  cursor: pointer;
  background-color: rgba(0, 0, 0, 0); /* 透明背景 */
}

/* 添加新的样式 */
.mapping-card-back {
    cursor: pointer;
}

.mapping-card-back .back-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

/* 已添加状态的样式 */
.mapping-card.added .mapping-card-back {
    background-color: #67c23a;
}

/* 禁用状态的样式 */
.mapping-card-back.disabled {
    background-color: #909399;
    cursor: not-allowed;
}

/* 重置背景色为白色 */
.mapping-card.reset-background .mapping-card-front {
  border: 1px solid #dcdcdc; /* 悬停时的浅边框颜色 */
  border-radius: 8px;
  transition: border 0.2s;
  background-color: #ffffff !important;  /* 使用 !important 确保覆盖其他状态 */
}

/* 深色模式下的背景色 */
@media (prefers-color-scheme: dark) {
  .mapping-card.reset-background .mapping-card-front {
    background-color: #1c1c1e !important;
  }
}

/* 确保勾号显示在白色背景上 */
.mapping-card.reset-background .mapping-card-front::after {
  color: #34C759;
  font-size: 14px;
  font-weight: bold;
}

/* 添加平滑过渡效果 */
.mapping-card-front {
  transition: background-color 0.3s ease;
}

/* 完全正确的样式 */
.correct .mapping-card-front {
  background-color: #e0ffe0; /* 浅绿色 */
}

/* 部分正确的样式 */
.partially-correct .mapping-card-front {
  background-color: #fff4e0; /* 浅橙色 */
  border: 1px solid #ffa940; /* 橙色边框 */
}

/* 错误的样式 */
.incorrect .mapping-card-front {
  background-color: #ffe0e0; /* 浅红色 */
}

/* 深色模式适配 */
@media (prefers-color-scheme: dark) {
  .correct .mapping-card-front {
    background-color: #2ecc71; /* 深绿色 */
  }

  .partially-correct .mapping-card-front {
    background-color: #d4a017; /* 深橙色 */
    border: 1px solid #ffa940;
  }

  .incorrect .mapping-card-front {
    background-color: #e74c3c; /* 深红色 */
  }

  .mapping-button {
    padding: 10px 20px; /* 按钮内边距 */
    font-size: 16px; /* 按钮字体大小 */
    border: none; /* 去掉默认边框 */
    border-radius: 5px; /* 圆角 */
    cursor: pointer; /* 鼠标悬停时显示为指针 */
    transition: background-color 0.3s; /* 背景颜色过渡效果 */
    width: 100%; /* 按钮宽度占满父容器 */
    text-align: center; /* 文字居中 */
    margin-bottom: 10px; /* 按钮之间的间距 */
  }

  .mapping-button:last-child {
    margin-bottom: 0; /* 最后一个按钮没有底部间距 */
  }

  .mapping-button:disabled {
    background-color: #ccc; /* 禁用状态下的背景颜色 */
    cursor: not-allowed; /* 禁用状态下的鼠标样式 */
  }

  .mapping-button:not(:disabled) {
    background-color: #ffffff; /* 正常状态下的背景颜色 */
    color: #007aff; /* 正常状态下的文字颜色 */
  }

  .mapping-button:not(:disabled):hover {
    background-color: #e0e0e0; /* 悬停状态下的背景颜色 */
  }
}
</style>




