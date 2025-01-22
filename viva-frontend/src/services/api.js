import axios from 'axios';
import {useUserStore} from '@/stores/user';

//const API_URL = 'https://viva.liugongzi.org/api';
const API_URL = 'http://localhost:8000';
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  withCredentials: true
});

// 添加请求拦截器来设置 JWT token，以后所有的请求都带了能表示用户身份的 token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('jwt_token');
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const userStore = useUserStore();
    
    // 统一处理认证失败的情况
    if (error.response?.data?.detail === 'Could not validate credentials' || 
        error.response?.status === 401) {
      // 清除认证信息
      localStorage.removeItem('jwt_token');
      userStore.logout();
      
      // 重新初始化 Google 登录
      if (window.google?.accounts) {
        window.google.accounts.id.prompt();
      }
      
      // 显示统一的 Toast 提示
      showGlobalToast('登录已过期，请重新登录', 'error');
    }
    
    return Promise.reject(error);
  }
);

// 全局 Toast 显示函数
function showGlobalToast(message, type = 'error') {
  // 创建一个事件来触发 Toast
  const event = new CustomEvent('show-toast', {
    detail: { message, type }
  });
  window.dispatchEvent(event);
}

export default {
  // 获取文章列表
  getEssays() {
    return api.get('/essays');
  },

  // 提交新文章
  submitEssay(content, image = null) {
    const formData = new FormData();
    formData.append('content', content);
    
    if (image) {
      formData.append('image', image);
    }

    return api.post('/submitEssay', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },


  // 获取句子列表
  getEssaySentenceIds(essay_id) {
    return api.get(`/essays/${essay_id}/sentences`);
  },

  getSentenceWithMappings(sentence_id) {
    return api.get(`/sentence/${sentence_id}`); 
  },

  // 验证 Google Token
  verifyGoogleToken(token) {
    return api.post('/auth/google-login', { token })
      .then(response => {
        // 存储 JWT token
        if (response.data.token) {
          localStorage.setItem('jwt_token', response.data.token);
        }
        return response.data;
      })
      .catch(error => {
        console.error('Google token verification failed:', error);
        throw error;
      });
  },

  // 获取用户信息
  getUserInfo() {
    return api.get('/user/info');
  },

  // 添加单词到 Anki
  addWordToAnki(sentence, mapping_chinese, mapping_wrong_english, mapping_correct_english) {
    return api.post('/mapping/addToAnki', { sentence, mapping_chinese, mapping_wrong_english, mapping_correct_english });
  },
  // 可以添加更多 API 调用方法...

  // 添加单词复习
  addWordToReview(word, wrong_word, translation, example_sentence) {
    console.log('addWordToReview', word, wrong_word, translation, example_sentence);
    return api.post('/word', { word, wrong_word, translation, example_sentence });
  },

  getWordReviewCount() {
    return api.get('/word/review/count');
  },

  getWordReviewList() {
    return api.get('/word/review/list');
  },

  getWordReviewInfo(word_id) {
    return api.get(`/word/review/${word_id}`);
  },

  putWordReview(id, quality) {
    return api.put('/word', { id, quality });
  },

  postWordReviewKnow(id, is_know) {
    return api.post('/word/known', { id, is_know });
  },

  getReviewStat() {
    return api.get(`/word/review/stat`);
  },

  getReviewDayStat(start_date, end_date) {
    return api.get(`/word/review/dayStat?start_date=${start_date}&end_date=${end_date}`);
  }
};
