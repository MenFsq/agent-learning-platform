<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h1 class="login-title">Agent Learning Platform</h1>
        <p class="login-subtitle">AI Agent学习平台 - 登录</p>
      </div>

      <el-form 
        ref="loginFormRef" 
        :model="loginForm" 
        :rules="loginRules" 
        class="login-form"
        @submit.prevent="handleLogin"
      >
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="用户名"
            size="large"
            :prefix-icon="User"
          />
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="密码"
            size="large"
            :prefix-icon="Lock"
            show-password
          />
        </el-form-item>

        <el-form-item>
          <el-checkbox v-model="loginForm.remember">记住我</el-checkbox>
          <el-link type="primary" class="forgot-password">忘记密码？</el-link>
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            size="large"
            class="login-button"
            :loading="loading"
            @click="handleLogin"
          >
            登录
          </el-button>
        </el-form-item>

        <div class="login-footer">
          <p class="demo-account">
            <strong>演示账号:</strong> admin / admin123
          </p>
          <p class="quick-login">
            快速登录: 
            <el-button type="text" @click="quickLogin('admin')">管理员</el-button>
            <el-button type="text" @click="quickLogin('user')">普通用户</el-button>
            <el-button type="text" @click="quickLogin('guest')">访客</el-button>
          </p>
        </div>
      </el-form>

      <div class="login-features">
        <h3>平台功能</h3>
        <ul>
          <li>📊 项目仪表板和进度跟踪</li>
          <li>📚 AI Agent学习指南和教程</li>
          <li>💻 代码示例和实战项目</li>
          <li>🤝 BotLearn社区集成</li>
          <li>🚀 前后端分离现代化架构</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'

const router = useRouter()
const loginFormRef = ref<FormInstance>()
const loading = ref(false)

// 登录表单
const loginForm = reactive({
  username: '',
  password: '',
  remember: false
})

// 表单验证规则
const loginRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
  ]
}

// 处理登录
const handleLogin = async () => {
  if (!loginFormRef.value) return

  const valid = await loginFormRef.value.validate()
  if (!valid) return

  loading.value = true

  try {
    // 模拟API调用延迟
    await new Promise(resolve => setTimeout(resolve, 1000))

    // 模拟登录成功
    const token = `mock-token-${Date.now()}`
    localStorage.setItem('token', token)
    localStorage.setItem('user', JSON.stringify({
      id: 1,
      username: loginForm.username,
      name: loginForm.username === 'admin' ? '管理员' : '用户',
      role: loginForm.username === 'admin' ? 'admin' : 'user',
      avatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'
    }))

    // 记住我功能
    if (loginForm.remember) {
      localStorage.setItem('rememberedUser', loginForm.username)
    } else {
      localStorage.removeItem('rememberedUser')
    }

    ElMessage.success('登录成功！')
    
    // 跳转到首页
    router.push('/')
  } catch (error) {
    ElMessage.error('登录失败，请检查用户名和密码')
  } finally {
    loading.value = false
  }
}

// 快速登录
const quickLogin = (type: string) => {
  if (type === 'admin') {
    loginForm.username = 'admin'
    loginForm.password = 'admin123'
  } else if (type === 'user') {
    loginForm.username = 'user'
    loginForm.password = 'user123'
  } else {
    loginForm.username = 'guest'
    loginForm.password = 'guest123'
  }
  
  // 自动触发登录
  setTimeout(() => {
    handleLogin()
  }, 100)
}
</script>

<style scoped>
.login-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 420px;
  background: white;
  border-radius: 16px;
  padding: 40px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.login-title {
  font-size: 28px;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.login-subtitle {
  font-size: 16px;
  color: #666;
}

.login-form {
  margin-bottom: 32px;
}

.login-button {
  width: 100%;
  height: 48px;
  font-size: 16px;
  font-weight: 600;
}

.forgot-password {
  float: right;
}

.login-footer {
  text-align: center;
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #eee;
}

.demo-account {
  font-size: 14px;
  color: #666;
  margin-bottom: 12px;
}

.quick-login {
  font-size: 14px;
  color: #666;
}

.login-features {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #eee;
}

.login-features h3 {
  font-size: 18px;
  color: #333;
  margin-bottom: 16px;
  text-align: center;
}

.login-features ul {
  list-style: none;
  padding: 0;
}

.login-features li {
  padding: 8px 0;
  color: #555;
  font-size: 14px;
  display: flex;
  align-items: center;
}

.login-features li::before {
  content: '✓';
  color: #67c23a;
  font-weight: bold;
  margin-right: 8px;
}

/* 响应式设计 */
@media (max-width: 480px) {
  .login-card {
    padding: 24px;
  }
  
  .login-title {
    font-size: 24px;
  }
}
</style>