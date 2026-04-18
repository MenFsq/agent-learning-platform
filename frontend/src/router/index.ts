import { createRouter, createWebHashHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: {
      title: '仪表板'
    }
  },
  {
    path: '/projects',
    name: 'Projects',
    component: () => import('@/views/Projects.vue'),
    meta: {
      title: '项目管理'
    }
  },
  {
    path: '/agent',
    name: 'Agent',
    component: () => import('@/views/Agent.vue'),
    meta: {
      title: 'Agent工作台'
    }
  },
  {
    path: '/learning',
    name: 'Learning',
    component: () => import('@/views/Learning.vue'),
    meta: {
      title: '学习指南'
    }
  },
  {
    path: '/community',
    name: 'Community',
    component: () => import('@/views/Community.vue'),
    meta: {
      title: '社区动态'
    }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/views/Settings.vue'),
    meta: {
      title: '系统设置'
    }
  },
  {
    path: '/api-docs',
    name: 'ApiDocs',
    component: () => import('@/views/ApiDocs.vue'),
    meta: {
      title: 'API文档'
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: {
      title: '登录',
      public: true // 标记为公开页面
    }
  },
  {
    path: '/test',
    name: 'Test',
    component: () => import('@/views/TestConnection.vue'),
    meta: {
      title: '连接测试'
    }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
    meta: {
      title: '页面未找到'
    }
  }
]

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - Agent Learning Platform`
  }

  const token = localStorage.getItem('token')
  const isPublicPage = to.meta.public

  if (!token && !isPublicPage) {
    // 如果用户未登录且访问的是非公开页面，则重定向到登录页
    return next('/login')
  } else if (token && to.path === '/login') {
    // 如果用户已登录且访问的是登录页，则重定向到首页
    return next('/')
  } else {
    // 其他情况正常访问
    next()
  }
})

export default router