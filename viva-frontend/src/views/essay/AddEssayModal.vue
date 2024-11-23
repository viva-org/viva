<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <div class="add-essay">
        <h2 class="title">新建想法</h2>
        <div class="essay-form">
          <div class="user-info">
            <img :src="userAvatar" alt="User Avatar" class="avatar">
            <span class="username">{{ username }}</span>
          </div>
          <textarea
            v-model="content"
            placeholder="写写串文..."
            class="essay-content"
          ></textarea>
          <div class="action-buttons">
            <label for="image-upload" class="action-btn">
              <i class="icon">🖼️</i>
              <input 
                id="image-upload" 
                type="file" 
                @change="handleImageUpload" 
                accept="image/*" 
                style="display: none;"
              >
            </label>
            <button class="action-btn"><i class="icon">GIF</i></button>
            <button class="action-btn"><i class="icon">#</i></button>
            <button class="action-btn"><i class="icon">≡</i></button>
          </div>
          <div v-if="imagePreview" class="image-preview">
            <img :src="imagePreview" alt="Image Preview" />
            <button @click="removeImage" class="remove-image">×</button>
          </div>
          <div class="visibility-option">
            <span class="visibility-icon">👤</span>
            <span>Post 你的世界观，稍后用英语再表达一次！</span>
          </div>
          <button @click="submitEssay" class="submit-btn">发布</button>
        </div>
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
    const image = ref(null);
    const imagePreview = ref(null);
    const userAvatar = ref('path/to/default/avatar.png'); // 替换为实际的用户头像路径
    const username = ref('luisleonard75'); // 替换为实际的用户名

    const handleImageUpload = (event) => {
      const file = event.target.files[0];
      if (file) {
        image.value = file;
        const reader = new FileReader();
        reader.onload = (e) => {
          imagePreview.value = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    };

    const removeImage = () => {
      image.value = null;
      imagePreview.value = null;
    };

    const submitEssay = async () => {
      try {
        await api.submitEssay(content.value, image.value);
        content.value = '';
        image.value = null;
        imagePreview.value = null;
        emit('close');
        emit('essay-published');
      } catch (error) {
        console.error('提交文章错误:', error);
      }
    };

    return {
      content,
      userAvatar,
      username,
      imagePreview,
      handleImageUpload,
      removeImage,
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
  border-radius: 16px;
  padding: 20px;
  max-width: 600px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.add-essay {
  width: 100%;
}

.title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 20px;
}

.essay-form {
  display: flex;
  flex-direction: column;
}

.user-info {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  margin-right: 10px;
}

.username {
  font-weight: bold;
}

.essay-content {
  width: 100%;
  height: 150px;
  border: none;
  resize: none;
  font-size: 16px;
  margin-bottom: 15px;
}

.action-buttons {
  display: flex;
  margin-bottom: 15px;
}

.action-btn {
  background: none;
  border: none;
  font-size: 20px;
  margin-right: 15px;
  cursor: pointer;
}

.visibility-option {
  display: flex;
  align-items: center;
  font-size: 14px;
  color: #555;
  margin-bottom: 15px;
}

.visibility-icon {
  margin-right: 5px;
}
</style>
