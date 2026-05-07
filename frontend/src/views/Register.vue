<template>
  <div class="login-container">
    <div class="ambient-grid"></div>
    <div class="ambient-orb ambient-orb-left"></div>
    <div class="ambient-orb ambient-orb-right"></div>

    <div class="login-shell">
      <section class="brand-panel">
        <div class="brand-headline">
          <div class="brand-mark">
            <span class="brand-mark-core"></span>
          </div>
          <div class="brand-copy">
            <p class="login-eyebrow">Agent Workspace</p>
            <span class="brand-status">Join the platform</span>
          </div>
        </div>

        <p class="brand-caption">AI agent workflow cockpit</p>
        <h1 class="login-title text-gradient">创建账号</h1>
        <p class="login-subtitle">
          注册后即可访问项目管理、学习路线、部署检查等全部工作台功能。
        </p>

        <div class="dynamic-stage">
          <div class="stage-grid"></div>
          <div class="stage-core">
            <p class="feature-panel-label">Get Started</p>
            <strong>注册即用</strong>
            <p>一对极简表单即可开启完整的 Agent 工作流体验。</p>
          </div>
        </div>
      </section>

      <section class="login-card">
        <div class="login-card-body">
          <div class="card-glow-line"></div>

          <div class="login-header">
            <p class="panel-tag">Register</p>
            <h2>注册新账号</h2>
            <p>填写以下信息创建您的工作台账号。</p>
          </div>

          <el-form
            ref="registerFormRef"
            :model="registerForm"
            :rules="registerRules"
            class="login-form"
            @submit.prevent="handleRegister"
          >
            <el-form-item prop="username">
              <el-input
                v-model="registerForm.username"
                placeholder="用户名（3-20位）"
                size="large"
                :prefix-icon="User"
              />
            </el-form-item>

            <el-form-item prop="email">
              <el-input
                v-model="registerForm.email"
                placeholder="邮箱地址"
                size="large"
                :prefix-icon="Message"
              />
            </el-form-item>

            <el-form-item prop="password">
              <el-input
                v-model="registerForm.password"
                type="password"
                placeholder="密码（至少6位）"
                size="large"
                :prefix-icon="Lock"
                show-password
              />
            </el-form-item>

            <el-form-item prop="confirmPassword">
              <el-input
                v-model="registerForm.confirmPassword"
                type="password"
                placeholder="确认密码"
                size="large"
                :prefix-icon="Lock"
                show-password
              />
            </el-form-item>

            <el-button
              type="primary"
              size="large"
              class="login-button"
              :loading="loading"
              @click="handleRegister"
            >
              注册并进入工作台
            </el-button>

            <div class="login-footer">
              <div class="register-link">
                <span>已有账号？</span>
                <el-link type="primary" @click="goLogin">返回登录</el-link>
              </div>
            </div>
          </el-form>
        </div>
      </section>
    </div>
    <footer class="login-page-footer">
      © 2026 Agent Learning Platform Contributors · Licensed under the MIT License
    </footer>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, Message } from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'

import { authAPI } from '@/api/index.ts'

const router = useRouter()
const registerFormRef = ref<FormInstance>()
const loading = ref(false)

const registerForm = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const validateConfirmPassword = (_rule: unknown, value: string, callback: (error?: Error) => void) => {
  if (value !== registerForm.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const registerRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 64, message: '密码长度至少 6 位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

const getErrorMessage = (error: unknown) => {
  if (
    typeof error === 'object' &&
    error !== null &&
    'response' in error &&
    typeof error.response === 'object' &&
    error.response !== null &&
    'data' in error.response
  ) {
    const data = (error.response as { data?: { detail?: string } }).data
    if (data?.detail) return data.detail
  }
  return '注册失败，请稍后重试'
}

const handleRegister = async () => {
  if (!registerFormRef.value) return

  try {
    await registerFormRef.value.validate()
  } catch {
    return
  }

  loading.value = true

  try {
    const response = await authAPI.register({
      username: registerForm.username,
      email: registerForm.email,
      password: registerForm.password
    })

    const { access_token, refresh_token, user_id, username } = response.data
    localStorage.setItem('token', access_token)
    localStorage.setItem('refresh_token', refresh_token)
    localStorage.setItem('user', JSON.stringify({
      id: user_id,
      username,
      email: registerForm.email,
      name: username,
      role: 'user',
      avatar: `https://api.dicebear.com/7.x/bottts/svg?seed=${encodeURIComponent(username)}`
    }))

    ElMessage.success('注册成功！')
    router.push('/')
  } catch (error) {
    ElMessage.error(getErrorMessage(error))
  } finally {
    loading.value = false
  }
}

const goLogin = () => {
  router.push('/login')
}
</script>

<style scoped lang="scss">
@use '@/styles/mixins' as *;

.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: clamp(16px, 3vw, 28px);
  position: relative;
  overflow: hidden;
}

.ambient-grid,
.ambient-orb {
  position: absolute;
  pointer-events: none;
}

.ambient-grid {
  inset: 0;
  opacity: 0.16;
  background-image:
    linear-gradient(var(--hero-grid) 1px, transparent 1px),
    linear-gradient(90deg, var(--hero-grid) 1px, transparent 1px);
  background-size: 108px 108px;
  mask-image: radial-gradient(circle at center, black 30%, transparent 82%);
}

.ambient-orb {
  width: 440px;
  height: 440px;
  border-radius: 999px;
  filter: blur(36px);
  opacity: 0.4;
}

.ambient-orb-left {
  top: 10%;
  left: -120px;
  background: radial-gradient(circle, rgba(59, 130, 246, 0.22), transparent 68%);
}

.ambient-orb-right {
  right: -140px;
  bottom: 4%;
  background: radial-gradient(circle, rgba(139, 92, 246, 0.22), transparent 68%);
}

.login-shell {
  width: min(1120px, 100%);
  display: grid;
  grid-template-columns: minmax(0, 1.1fr) minmax(360px, 420px);
  gap: clamp(18px, 3vw, 32px);
  align-items: stretch;
  position: relative;
  z-index: 1;
}

.login-page-footer {
  position: absolute;
  left: 50%;
  bottom: clamp(16px, 2.5vw, 24px);
  transform: translateX(-50%);
  color: var(--text-muted);
  font-size: 12px;
  line-height: 1.6;
  z-index: 1;
}

.brand-panel {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 18px;
  padding: clamp(4px, 1vw, 12px);
}

.brand-headline {
  display: inline-flex;
  align-items: center;
  gap: 16px;
}

.brand-mark {
  width: 54px;
  height: 54px;
  border-radius: 18px;
  display: grid;
  place-items: center;
  background:
    radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.46), transparent 36%),
    linear-gradient(135deg, rgba(59, 130, 246, 0.95), rgba(139, 92, 246, 0.92));
}

.brand-mark-core {
  width: 18px;
  height: 18px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.95);
}

.brand-copy {
  display: grid;
  gap: 6px;
}

.brand-caption {
  margin: 0;
  color: var(--text-muted);
  font-size: 11px;
  letter-spacing: 0.24em;
  text-transform: uppercase;
}

.brand-status {
  color: var(--text-secondary);
  font-size: 13px;
}

.login-eyebrow,
.feature-panel-label,
.panel-tag {
  margin: 0;
  color: var(--color-secondary);
  font-size: 11px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
}

.login-title {
  margin: 0;
  font-size: clamp(34px, 5.4vw, 58px);
  line-height: 0.98;
}

.login-subtitle {
  margin: 0;
  max-width: 680px;
  color: var(--text-secondary);
  font-size: 15px;
  line-height: 1.7;
}

.login-card {
  @include section-shell;
  height: 100%;
  padding: clamp(22px, 3vw, 28px);
  background: rgba(255, 255, 255, 0.06);
  border-radius: var(--radius-xl);
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 18px;
}

.card-glow-line {
  width: 120px;
  height: 4px;
  border-radius: 999px;
  margin-bottom: 16px;
  background: linear-gradient(90deg, var(--color-primary), var(--color-secondary), var(--color-accent));
}

.login-card-body {
  display: grid;
  gap: 0;
}

.login-header {
  display: grid;
  gap: 8px;
  margin-bottom: 18px;
}

.login-header h2 {
  margin: 0;
  font-size: clamp(24px, 3.2vw, 30px);
  color: var(--text-primary);
}

.login-header p:last-child {
  margin: 0;
  color: var(--text-secondary);
  line-height: 1.6;
  font-size: 14px;
}

.login-form {
  display: grid;
  gap: 8px;
}

.login-form :deep(.el-form-item) {
  margin-bottom: 8px;
}

.login-form :deep(.el-input__wrapper) {
  min-height: 46px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.04);
  box-shadow: inset 0 0 0 1px var(--line-soft);
}

.login-form :deep(.el-input__wrapper.is-focus) {
  background: rgba(255, 255, 255, 0.07);
  box-shadow:
    inset 0 0 0 1px rgba(59, 130, 246, 0.5),
    0 0 0 4px rgba(59, 130, 246, 0.12);
}

.login-form :deep(.el-input__inner) {
  color: var(--text-primary);
}

.login-button {
  width: 100%;
  min-height: 46px;
  margin-top: 8px;
  border: none;
  border-radius: 14px;
  font-size: 14px;
  font-weight: 700;
  background: linear-gradient(135deg, var(--color-primary), var(--color-accent));
}

.login-footer {
  display: flex;
  justify-content: center;
  padding-top: 12px;
}

.register-link {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--text-secondary);
  font-size: 14px;
}

.dynamic-stage {
  flex: 0 0 auto;
  position: relative;
  min-height: 330px;
  padding: 20px;
  border-radius: 32px;
  border: 1px solid var(--line-soft);
  background:
    radial-gradient(circle at 50% 50%, rgba(59, 130, 246, 0.12), transparent 28%),
    linear-gradient(180deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.02));
  overflow: hidden;
}

.stage-grid {
  position: absolute;
  inset: 0;
  z-index: 0;
  opacity: 0.18;
  background-image:
    linear-gradient(var(--hero-grid) 1px, transparent 1px),
    linear-gradient(90deg, var(--hero-grid) 1px, transparent 1px);
  background-size: 72px 72px;
  mask-image: radial-gradient(circle at center, black 38%, transparent 82%);
}

.stage-core {
  position: absolute;
  inset: 50% auto auto 50%;
  z-index: 4;
  transform: translate(-50%, -50%);
  width: min(288px, calc(100% - 48px));
  padding: 20px 18px;
  text-align: center;
  border-radius: 28px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(15, 23, 42, 0.42);
  backdrop-filter: blur(18px);
}

.stage-core strong {
  display: block;
  margin-top: 8px;
  font-size: clamp(20px, 3vw, 28px);
  line-height: 1.15;
}

.stage-core p:last-child {
  margin: 8px 0 0;
  color: var(--text-secondary);
  line-height: 1.6;
  font-size: 14px;
}

@media (max-width: 980px) {
  .login-shell {
    grid-template-columns: 1fr;
    max-width: 720px;
  }
}

@media (max-width: 640px) {
  .login-container {
    padding: 18px 18px 56px;
  }
  .dynamic-stage {
    min-height: 240px;
  }
}
</style>
