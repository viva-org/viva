import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  // 第一类型的布局
  {
    path: '/',
    component: () => import('@/layouts/MainLayout.vue'),
    children: [
      // 默认的页面
      {
        path: '',
        name: 'essay-list',
        component: () => import('@/views/essay/EssayList.vue'),
        meta: { 
          layout: 'main',
          requiresAuth: false 
        }
      },
      // ... 其他需要主布局的路由
    ]
  },
  // 第二类型的布局
  {
    path: '/login',
    component: () => import('@/layouts/AuthLayout.vue'),
    children: [

    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router