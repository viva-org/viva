<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <div class="modal-header">
        <h2>新想法</h2>
      </div>
      <div class="modal-body">
        <div class="form-group">
          <div class="input-container">
            <label class="form-label">Essay</label>
            <textarea 
              v-model="content"
              class="form-input"
              placeholder="把你的想法粘贴在这里，想法是不分语言的，给我一个中文想法，LEXICON AI 会帮你塑造你的英文能力，
Attention is all you need！"
            ></textarea>
          </div>
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn-cancel" @click="$emit('close')">Cancel</button>
        <button @click="submitEssay" class="btn-create">Create</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import api from '@/services/api';

export default {
  name: 'AddEssay',
  setup(props, { emit }) {
    const content = ref('');

    const submitEssay = async () => {
      try {
        await api.submitEssay(content.value);
        content.value = '';
        emit('close');
        emit('essay-published');
      } catch (error) {
        console.error('提交文章错误:', error);
      }
    };

    return {
      content,
      submitEssay
    };
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
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 8px;
  width: 550px;
  max-width: 90vw;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.modal-header {
  padding: 24px 24px 16px;
  background: transparent;
}

.modal-header h2 {
  margin: 0;
  font-size: 22px;
  font-weight: 400;
  color: #202124;
}

.modal-body {
  padding: 24px;
  background: transparent;
}

.form-group {
  position: relative;
}

.input-container {
  position: relative;
}

.form-label {
  position: absolute;
  top: -6px;
  left: 10px;
  font-size: 12px;
  font-weight: 500;
  color: #202124;
  background-color: white;
  padding: 0 4px;
  z-index: 1;
  text-transform: uppercase;
}

.form-input {
  width: 100%;
  height: 120px;
  padding: 12px;
  font-size: 16px;
  border: 2px solid #202124;
  border-radius: 4px;
  color: #202124;
  background: transparent;
  transition: all 0.2s;
  box-sizing: border-box;
  resize: none;
  line-height: 1.5;
}

.form-input:focus {
  outline: none;
  border-color: #202124;
  box-shadow: 0 0 0 1px #202124;
}

.form-input::placeholder {
  color: #5f6368;
}

.modal-footer {
  padding: 16px 24px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  background: transparent;
}

.btn-cancel {
  padding: 8px 24px;
  font-size: 14px;
  font-weight: 500;
  color: #202124;
  background: none;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-cancel:hover {
  background-color: rgba(32, 33, 36, 0.04);
}

.btn-create {
  padding: 8px 24px;
  font-size: 14px;
  font-weight: 500;
  color: white;
  background-color: #202124;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-create:hover {
  background-color: #000000;
}

.btn-create:disabled {
  background-color: #dadce0;
  cursor: not-allowed;
}
</style>
