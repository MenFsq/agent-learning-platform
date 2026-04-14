import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import '@vue-flow/core/dist/style.css'
import '@vue-flow/core/dist/theme-default.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

import App from './App.vue'
import router from './router'

import './styles/global.scss'

// 开发环境：添加模拟token
if (import.meta.env.DEV) {
  console.log('开发环境：设置模拟token')
  localStorage.setItem('token', 'dev-mock-token-123456')
  localStorage.setItem('user', JSON.stringify({
    id: 1,
    name: '小老虎 🐯',
    email: 'tiger@agent-learning.com',
    role: 'admin'
  }))
}

const app = createApp(App)

// 注册Element Plus图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(createPinia())
app.use(router)
app.use(ElementPlus)

app.mount('#app')