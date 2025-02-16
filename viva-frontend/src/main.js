// src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from '@/router'
import pinia from '@/stores'
import googleAuth from '@/plugins/googleAuth'
import 'remixicon/fonts/remixicon.css'
import '@/styles/main.scss'  // 导入自己定义的网站的整个样式体系

// 引入 Element Plus 样式
import 'element-plus/dist/index.css'

const app = createApp(App)

app.use(router)
app.use(pinia)
app.use(googleAuth)

app.mount('#app')