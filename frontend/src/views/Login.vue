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
            <span class="brand-status">Live workflow orchestration</span>
          </div>
        </div>

        <p class="brand-caption">AI agent workflow cockpit</p>
        <h1 class="login-title text-gradient">Agent Learning Platform</h1>
        <p class="login-subtitle">
          用一套更轻、更流动的工作台，把项目推进、学习路线和部署检查组织在同一个上下文里。
        </p>

        <div class="dynamic-stage">
          <div class="stage-grid"></div>
          <div class="stage-core">
            <p class="feature-panel-label">Live Canvas</p>
            <strong>One context, multiple lanes</strong>
            <p>项目、学习、部署和反馈在一张动态画布里持续联动。</p>
          </div>

          <article
            v-for="node in orbitNodes"
            :key="node.title"
            class="orbit-node"
            :class="node.className"
          >
            <span>{{ node.label }}</span>
            <strong>{{ node.title }}</strong>
            <p>{{ node.detail }}</p>
          </article>
        </div>
      </section>

      <section class="login-card">
        <div class="login-card-body">
          <div class="card-glow-line"></div>

          <div class="login-header">
            <p class="panel-tag">Sign In</p>
            <h2>登录进入工作台</h2>
            <p>输入账号信息后即可继续访问项目与学习内容。</p>
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

            <div class="login-options">
              <el-checkbox v-model="loginForm.remember">记住我</el-checkbox>
              <el-link type="primary" class="forgot-password">忘记密码？</el-link>
            </div>

            <el-button
              type="primary"
              size="large"
              class="login-button"
              :loading="loading"
              @click="handleLogin"
            >
              登录并进入工作台
            </el-button>

            <div class="login-footer">
              <div class="demo-account">
                <span>演示账号</span>
                <strong class="metric-mono">admin / admin123</strong>
              </div>

              <div class="quick-login">
                <span class="quick-login-label">快速登录</span>
                <div class="quick-login-actions">
                  <button type="button" class="quick-login-chip" @click="quickLogin('admin')">管理员</button>
                  <button type="button" class="quick-login-chip" @click="quickLogin('user')">普通用户</button>
                  <button type="button" class="quick-login-chip" @click="quickLogin('guest')">访客</button>
                </div>
              </div>
            </div>
          </el-form>
        </div>

        <div class="login-support">
          <p class="login-support-label">登录后可继续</p>
          <div class="login-support-grid">
            <article class="support-item">
              <strong>项目上下文</strong>
              <p>继续上一次的项目推进节奏与任务状态。</p>
            </article>
            <article class="support-item">
              <strong>学习路径</strong>
              <p>从当前阶段恢复课程和知识地图浏览进度。</p>
            </article>
          </div>
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
import { User, Lock } from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'

const orbitNodes = [
  {
    label: 'Project Pulse',
    title: 'Sprint Stream',
    detail: '把冲刺进度、任务风险和今日优先级收拢在同一层。',
    className: 'is-project'
  },
  {
    label: 'Learning Route',
    title: 'Path Context',
    detail: '学习路线会沿着当前阶段自动保持连续节奏。',
    className: 'is-learning'
  },
  {
    label: 'Deploy Watch',
    title: 'Release Signal',
    detail: '部署检查、实验记录和反馈信号在这里同步更新。',
    className: 'is-release'
  }
]

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
  animation: ambient-drift 16s ease-in-out infinite;
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
  animation-delay: -7s;
}

.login-container::before,
.login-container::after {
  content: '';
  position: absolute;
  border-radius: 999px;
  filter: blur(12px);
  pointer-events: none;
}

.login-container::before {
  width: 320px;
  height: 320px;
  top: 8%;
  left: 6%;
  background: radial-gradient(circle, var(--page-glow-1), transparent 70%);
}

.login-container::after {
  width: 360px;
  height: 360px;
  right: 5%;
  bottom: 8%;
  background: radial-gradient(circle, var(--page-glow-3), transparent 72%);
}

.login-container::selection {
  background: rgba(59, 130, 246, 0.28);
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
  width: min(calc(100% - 32px), 1120px);
  color: var(--text-muted);
  font-size: 12px;
  line-height: 1.6;
  text-align: center;
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
  position: relative;
  background:
    radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.46), transparent 36%),
    linear-gradient(135deg, rgba(59, 130, 246, 0.95), rgba(139, 92, 246, 0.92));
  box-shadow:
    0 0 0 1px rgba(255, 255, 255, 0.12),
    0 24px 50px rgba(59, 130, 246, 0.28);
  animation: brand-pulse 6s ease-in-out infinite;
}

.brand-mark::before {
  content: '';
  position: absolute;
  inset: -8px;
  border-radius: 22px;
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.brand-mark-core {
  width: 18px;
  height: 18px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.95);
  box-shadow:
    0 0 22px rgba(255, 255, 255, 0.72),
    0 0 48px rgba(6, 182, 212, 0.5);
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
.panel-tag,
.quick-login-label,
.demo-account span {
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
  max-width: 10ch;
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

.dynamic-stage::before,
.dynamic-stage::after {
  content: '';
  position: absolute;
  inset: 50%;
  width: 280px;
  height: 280px;
  border-radius: 999px;
  transform: translate(-50%, -50%);
  pointer-events: none;
}

.dynamic-stage::before {
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow:
    0 0 0 36px rgba(255, 255, 255, 0.02),
    0 0 0 88px rgba(255, 255, 255, 0.015);
  animation: halo-rotate 22s linear infinite;
}

.dynamic-stage::after {
  background:
    conic-gradient(
      from 0deg,
      rgba(59, 130, 246, 0.32),
      rgba(6, 182, 212, 0.08),
      rgba(139, 92, 246, 0.3),
      rgba(59, 130, 246, 0.32)
    );
  filter: blur(28px);
  opacity: 0.4;
  animation: halo-rotate 18s linear infinite reverse;
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
  -webkit-backdrop-filter: blur(18px);
  box-shadow: 0 24px 60px rgba(6, 9, 16, 0.32);
}

.stage-core strong,
.stage-core p {
  display: block;
  margin: 0;
}

.stage-core strong {
  margin-top: 8px;
  font-size: clamp(20px, 3vw, 28px);
  line-height: 1.15;
}

.stage-core p:last-child {
  margin-top: 8px;
  color: var(--text-secondary);
  line-height: 1.6;
  font-size: 14px;
}

.orbit-node {
  --orbit-transform: translate3d(0, 0, 0);
  position: absolute;
  z-index: 2;
  width: min(196px, 44%);
  padding: 12px 14px;
  border-radius: 22px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(15, 23, 42, 0.34);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  box-shadow: 0 20px 44px rgba(6, 9, 16, 0.22);
  animation: node-float 9s ease-in-out infinite;
  transition:
    z-index 0s linear 0s,
    box-shadow var(--transition-base),
    border-color var(--transition-base),
    background var(--transition-base);
}

.orbit-node:hover {
  z-index: 8;
  border-color: rgba(96, 165, 250, 0.34);
  background: rgba(15, 23, 42, 0.56);
  box-shadow:
    0 0 0 1px rgba(59, 130, 246, 0.24),
    0 28px 56px rgba(6, 9, 16, 0.34);
}

.orbit-node span,
.orbit-node strong,
.orbit-node p {
  display: block;
  margin: 0;
}

.orbit-node span {
  color: var(--color-secondary);
  font-size: 10px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}

.orbit-node strong {
  margin-top: 6px;
  font-size: 15px;
}

.orbit-node p {
  margin-top: 6px;
  color: var(--text-secondary);
  line-height: 1.5;
  font-size: 13px;
}

.orbit-node.is-project {
  top: 18px;
  left: 18px;
}

.orbit-node.is-learning {
  top: 32px;
  right: 18px;
  animation-delay: -3s;
}

.orbit-node.is-release {
  left: 50%;
  bottom: 18px;
  --orbit-transform: translateX(-50%);
  animation-delay: -5s;
}

.login-card {
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

.login-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at top right, rgba(59, 130, 246, 0.16), transparent 34%),
    linear-gradient(160deg, rgba(255, 255, 255, 0.03), transparent 46%);
  pointer-events: none;
}

.card-glow-line {
  width: 120px;
  height: 4px;
  border-radius: 999px;
  margin-bottom: 16px;
  background: linear-gradient(90deg, var(--color-primary), var(--color-secondary), var(--color-accent));
  box-shadow: 0 0 26px rgba(59, 130, 246, 0.3);
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
  margin-bottom: 10px;
}

.login-form :deep(.el-input__wrapper) {
  min-height: 46px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.04);
  box-shadow: inset 0 0 0 1px var(--line-soft);
  transition:
    box-shadow var(--transition-base),
    background var(--transition-base);
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

.login-form :deep(.el-input__inner::placeholder) {
  color: var(--text-muted);
}

.login-form :deep(.el-checkbox) {
  color: var(--text-secondary);
}

.login-options {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 8px;
}

.forgot-password {
  font-size: 13px;
}

.login-button {
  width: 100%;
  min-height: 46px;
  margin-top: 2px;
  border: none;
  border-radius: 14px;
  font-size: 14px;
  font-weight: 700;
  background: linear-gradient(135deg, var(--color-primary), var(--color-accent));
  box-shadow: 0 18px 40px rgba(59, 130, 246, 0.22);
  position: relative;
  overflow: hidden;
}

.login-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 22px 42px rgba(59, 130, 246, 0.28);
}

.login-button::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(120deg, transparent 22%, rgba(255, 255, 255, 0.28) 50%, transparent 76%);
  transform: translateX(-120%);
  animation: button-sheen 4.6s ease-in-out infinite;
}

.login-footer {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid var(--line-soft);
  display: grid;
  gap: 14px;
}

.demo-account {
  display: grid;
  gap: 8px;
}

.demo-account strong {
  color: var(--text-primary);
  font-size: 14px;
}

.quick-login {
  display: grid;
  gap: 10px;
}

.quick-login-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.quick-login-chip {
  @include panel-hover;
  display: inline-flex;
  align-items: center;
  padding: 8px 12px;
  border-radius: 999px;
  border: 1px solid var(--line-soft);
  background: rgba(255, 255, 255, 0.04);
  color: var(--text-primary);
  cursor: pointer;
  font-size: 13px;
}

.login-support {
  position: relative;
  z-index: 1;
  padding-top: 16px;
  border-top: 1px solid var(--line-soft);
}

.login-support-label {
  margin: 0 0 10px;
  color: var(--color-secondary);
  font-size: 11px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
}

.login-support-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}

.support-item {
  padding: 12px 14px;
  border-radius: 18px;
  border: 1px solid var(--line-soft);
  background: rgba(255, 255, 255, 0.03);
}

.support-item strong,
.support-item p {
  margin: 0;
}

.support-item strong {
  color: var(--text-primary);
  font-size: 14px;
}

.support-item p {
  margin-top: 6px;
  color: var(--text-secondary);
  line-height: 1.55;
  font-size: 13px;
}

@keyframes ambient-drift {
  0%,
  100% {
    transform: translate3d(0, 0, 0) scale(1);
  }

  50% {
    transform: translate3d(18px, -14px, 0) scale(1.06);
  }
}

@keyframes brand-pulse {
  0%,
  100% {
    box-shadow:
      0 0 0 1px rgba(255, 255, 255, 0.12),
      0 24px 50px rgba(59, 130, 246, 0.28);
  }

  50% {
    box-shadow:
      0 0 0 1px rgba(255, 255, 255, 0.16),
      0 30px 58px rgba(59, 130, 246, 0.38);
  }
}

@keyframes halo-rotate {
  0% {
    transform: translate(-50%, -50%) rotate(0deg);
  }

  100% {
    transform: translate(-50%, -50%) rotate(360deg);
  }
}

@keyframes node-float {
  0%,
  100% {
    transform: var(--orbit-transform) translateY(0);
  }

  50% {
    transform: var(--orbit-transform) translateY(-8px);
  }
}

@keyframes button-sheen {
  0%,
  72%,
  100% {
    transform: translateX(-120%);
  }

  86% {
    transform: translateX(120%);
  }
}

@media (max-width: 980px) {
  .login-shell {
    grid-template-columns: 1fr;
    max-width: 720px;
  }

  .brand-panel {
    padding: 0;
    justify-content: flex-start;
  }

  .login-title {
    max-width: none;
  }

  .ambient-orb {
    width: 320px;
    height: 320px;
  }
}

@media (max-width: 640px) {
  .login-container {
    padding: 18px 18px 56px;
  }

  .login-card {
    min-width: 0;
  }

  .brand-headline {
    align-items: flex-start;
  }

  .dynamic-stage {
    min-height: 460px;
    padding: 20px;
  }

  .stage-core {
    position: relative;
    inset: auto;
    transform: none;
    width: 100%;
    margin-top: 150px;
  }

  .orbit-node {
    width: calc(100% - 24px);
  }

  .orbit-node.is-project {
    top: 18px;
    left: 12px;
  }

  .orbit-node.is-learning {
    top: 114px;
    right: 12px;
  }

  .orbit-node.is-release {
    left: 12px;
    bottom: 18px;
    --orbit-transform: translate3d(0, 0, 0);
  }

  .login-options {
    flex-direction: column;
    align-items: flex-start;
  }

  .quick-login-actions {
    width: 100%;
  }

  .quick-login-chip {
    flex: 1 1 calc(50% - 10px);
    justify-content: center;
  }

  .login-support-grid {
    grid-template-columns: 1fr;
  }

  .login-page-footer {
    width: calc(100% - 36px);
    bottom: 16px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .ambient-orb,
  .brand-mark,
  .dynamic-stage::before,
  .dynamic-stage::after,
  .orbit-node,
  .login-button::after {
    animation: none;
  }
}
</style>