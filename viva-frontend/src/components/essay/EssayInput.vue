<template>
  <div class="essay-input-card">
    <h2 class="card-header">
      <span>增加一个上传文章的</span>
      <span class="secondary-text">你脑子里的想法是？</span>
    </h2>
    <form @submit.prevent="handleSubmit" class="essay-form">
      <div class="textarea-wrapper">
        <textarea
          v-model="essayForm.text"
          placeholder="请输入你的中文作文..."
          rows="8"
          class="essay-textarea"
        ></textarea>
      </div>
      <button 
        type="submit" 
        class="submit-button" 
        :class="{ 'loading': loading }"
        :disabled="loading"
      >
        {{ loading ? '提交中...' : '提交' }}
      </button>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'EssayInput',
  props: {
    loading: Boolean
  },
  emits: ['essay-submitted'],
  setup(props, { emit }) {
    const essayForm = ref({ text: '' })

    const handleSubmit = () => {
      emit('essay-submitted', essayForm.value.text)
    }

    return {
      essayForm,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.essay-input-card {
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
  padding: 24px;
  margin-bottom: 32px;
}

.card-header {
  font-size: 20px;
  font-weight: 600;
  color: #1d1d1f;
  margin-bottom: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.secondary-text {
  font-size: 15px;
  color: #86868b;
  font-weight: normal;
}

.textarea-wrapper {
  background-color: #f5f5f7;
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 16px;
}

.essay-textarea {
  width: 100%;
  border: none;
  background-color: transparent;
  font-family: -apple-system, BlinkMacSystemFont, sans-serif;
  font-size: 17px;
  line-height: 1.5;
  color: #1d1d1f;
  resize: vertical;
}

.essay-textarea:focus {
  outline: none;
}

.submit-button {
  background-color: #0071e3;
  color: #ffffff;
  font-size: 17px;
  font-weight: 600;
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.submit-button:hover {
  background-color: #0077ed;
}

.submit-button.loading {
  opacity: 0.7;
  cursor: not-allowed;
}

@media (prefers-color-scheme: dark) {
  .essay-input-card {
    background-color: #1c1c1e;
  }

  .card-header {
    color: #f5f5f7;
  }

  .textarea-wrapper {
    background-color: #2c2c2e;
  }

  .essay-textarea {
    color: #f5f5f7;
  }

  .submit-button {
    background-color: #0a84ff;
  }

  .submit-button:hover {
    background-color: #0a8cff;
  }
}
</style>
