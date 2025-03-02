<template>
    <div class="sentence-detail">
        <div class="sentence-header">
            <span 
                v-for="(part, index) in processedSentence" 
                :key="index"
                :class="{ 'highlight-word': part.isHighlight }"
            >{{ part.text }}</span>
        </div>
        <div class="content-wrapper">
            <div class="mapping-input-container" ref="containerRef" tabindex="0" @keydown="handleKeydown">
                <MappingGridCard
                    :mappings="paginatedMappings"
                    :check-all-loading="checkAllLoading"
                    :show-results="showResults"
                    @update-input="handleUpdateInput"
                    @enter-pressed="handleEnterPressed"
                    @focus="handleFocus"
                    @add-to-anki="handleAddToAnki"
                    @add-to-review="handleAddToReview"
                />
            </div>
        </div>
    </div>
</template>

<script setup>
import {computed, nextTick, onMounted, provide, ref} from 'vue';
import MappingGridCard from '@/components/essay/MappingGridCard.vue';
import api from '@/services/api';

// Props
const props = defineProps({
    sentenceData: {
        type: Object,
        required: true
    },
    showResults: {
        type: Boolean,
        default: false
    }
});

// Reactive state
const sentence = computed(() => props.sentenceData?.sentence || {});
const mappingList = computed(() => props.sentenceData?.mappingList || []);
const inputs = ref({});

const currentPage = ref(1);
const containerRef = ref(null);
const checkAllLoading = ref(false);
const focusedWord = ref('');

// Provide inputs to child components
provide('inputs', inputs);

// Computed properties
const itemsPerPage = 100;
const totalPages = computed(() => Math.ceil(mappingList.value.length / itemsPerPage));
const paginatedMappings = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    return mappingList.value.slice(start, end);
});

// Methods




const handleUpdateInput = (focusWord, value) => {
    inputs.value[focusWord] = value;
    const mapping = mappingList.value.find(m => m.focus_word === focusWord);
    if (mapping) {
        mapping.translation = value;
    }
};

const handleEnterPressed = (index) => {
    console.log(`Enter pressed at index: ${index}`);
};

const handleFocus = (word) => {
    console.log('Focus on word:', word); // 调试日志
    nextTick(() => {
        focusedWord.value = word;
    });
};

const previousPage = () => {
    if (currentPage.value > 1) {
        currentPage.value--;
    }
};

const nextPage = () => {
    if (currentPage.value < totalPages.value) {
        currentPage.value++;
    }
};

const handleKeydown = (event) => {
    if (event.key === 'ArrowLeft') {
        previousPage();
    } else if (event.key === 'ArrowRight') {
        nextPage();
    }
};

// Lifecycle hooks
onMounted(() => {
    if (containerRef.value) {
        containerRef.value.focus();
    }
    // 初始化 inputs
    mappingList.value.forEach(mapping => {
        inputs.value[mapping.focus_word] = mapping.translation || '';
    });
});

const handleUpdateMapping = (updatedMapping) => {
    const index = mappingList.value.findIndex(m => m.id === updatedMapping.id);
    if (index !== -1) {
        mappingList.value[index] = updatedMapping;
    }
};

const computedMappings = computed({
    get: () => props.mappings,
    set: (newValue) => emit('update:mappings', newValue)
});


// 修改 highlightedSentence 以支持多字符高亮
const processedSentence = computed(() => {
    if (!focusedWord.value || !sentence.value.sentence) {
        return [{ text: sentence.value.sentence || '', isHighlight: false }];
    }

    const escapeRegExp = (string) => {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    };

    const parts = [];
    // 修改正则表达式以支持跨行匹配
    const regex = new RegExp(`(${escapeRegExp(focusedWord.value)})`, 'gim');
    let lastIndex = 0;
    let match;
    const sentenceText = sentence.value.sentence;

    while ((match = regex.exec(sentenceText)) !== null) {
        // 处理匹配前的文本，按换行符分割
        if (match.index > lastIndex) {
            const beforeText = sentenceText.slice(lastIndex, match.index);
            const lines = beforeText.split(/(\n)/);
            
            lines.forEach((line, i) => {
                if (line === '\n') {
                    parts.push({ text: '\n', isHighlight: false });
                } else if (line) {
                    parts.push({ text: line, isHighlight: false });
                }
            });
        }

        // 处理匹配的文本，按换行符分割
        const matchedText = match[0];
        const matchedLines = matchedText.split(/(\n)/);
        
        matchedLines.forEach((line, i) => {
            if (line === '\n') {
                parts.push({ text: '\n', isHighlight: false });
            } else if (line) {
                parts.push({ text: line, isHighlight: true });
            }
        });

        lastIndex = regex.lastIndex;
    }

    // 处理剩余文本，按换行符分割
    if (lastIndex < sentenceText.length) {
        const remainingText = sentenceText.slice(lastIndex);
        const lines = remainingText.split(/(\n)/);
        
        lines.forEach((line, i) => {
            if (line === '\n') {
                parts.push({ text: '\n', isHighlight: false });
            } else if (line) {
                parts.push({ text: line, isHighlight: false });
            }
        });
    }

    return parts;
});

const handleAddToAnki = (mapping) => {
    console.log(`Adding to Anki: ${mapping.focus_word}`);
    api.addWordToAnki(sentence.value.sentence, mapping.focus_word, mapping.translation, mapping.ai_review.ai_review_expression.replace(/[{}]/g, ''))
};

const handleAddToReview = (mapping) => {
    console.log(`Adding to Review: ${mapping.focus_word}`);
    api.addWordToReview(mapping.ai_review.ai_review_expression.replace(/[{}]/g, ''), mapping.translation, mapping.focus_word, sentence.value.sentence)
};

// Provide focusedWord to child components
provide('focusedWord', focusedWord);



</script>

<style scoped>
.sentence-detail {
    display: flex;
    flex-direction: column;
    height: 100%; /* 确保组件占满整个高度 */
    background-color: #f5f8f5;
    border: 1px solid #ddd;
    border-radius: 4px;
    overflow: hidden;
    width: 100%;
}

.sentence-header {
    display: inline-block;
    padding: 20px;
    background-color: #ffffff;
    border-bottom: 1px solid #ddd;
    font-size: 1.2em;
    line-height: 1.8;
    white-space: pre-wrap;
    word-wrap: break-word;
}

.highlight-word {
    position: relative;
    z-index: 1;
    white-space: pre-wrap;
}

.highlight-word::before {
    content: "";
    position: absolute;
    z-index: -1;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: var(--color-primary);
    border-radius: 3px;
}

.content-wrapper {
    flex: 1;
    overflow: hidden;
    position: relative;
}

.mapping-input-container {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    overflow-y: auto;
    padding: 20px;
    background-color: #ffffff;
}

/* 隐藏滚动条但保持功能 */
.mapping-input-container {
    scrollbar-width: none;
    -ms-overflow-style: none;
}

.mapping-input-container::-webkit-scrollbar {
    display: none;
}
</style>
