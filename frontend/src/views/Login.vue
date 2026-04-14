<template>
  <div class="login-container">
    <Particles id="login-particles" :options="particlesOptions as any" class="particles-layer" />
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

        <h1 class="login-title text-gradient">Agent Learning Platform</h1>
        <p class="login-subtitle">
          把项目推进、学习路径和社区反馈收拢到同一套工作台里，用更轻的界面承接你的 Agent 开发节奏。
        </p>

        <div class="brand-metrics">
          <article v-for="metric in platformMetrics" :key="metric.label" class="metric-card">
            <p>{{ metric.label }}</p>
            <strong class="metric-mono">{{ metric.value }}</strong>
            <span>{{ metric.detail }}</span>
          </article>
        </div>

        <div class="brand-feature-panel">
          <p class="feature-panel-label">进入平台后你会看到</p>
          <ul class="feature-list">
            <li v-for="feature in platformFeatures" :key="feature">{{ feature }}</li>
          </ul>
        </div>

        <div class="workspace-preview">
          <div class="preview-orbit" aria-hidden="true">
            <span class="orbit-ring orbit-ring-outer"></span>
            <span class="orbit-ring orbit-ring-inner"></span>
            <span class="orbit-node orbit-node-one"></span>
            <span class="orbit-node orbit-node-two"></span>
          </div>

          <div class="preview-surface">
            <div class="preview-header">
              <div>
                <p class="feature-panel-label">Workspace Preview</p>
                <strong>今日重点推进</strong>
              </div>
              <span class="preview-badge">Synced</span>
            </div>

            <div class="preview-flow">
              <article v-for="item in workspaceFlow" :key="item.title" class="preview-flow-item">
                <span class="preview-step-index metric-mono">{{ item.step }}</span>
                <div>
                  <strong>{{ item.title }}</strong>
                  <p>{{ item.detail }}</p>
                </div>
              </article>
            </div>

            <div class="preview-footer">
              <div v-for="item in previewSignals" :key="item.label" class="preview-signal">
                <span>{{ item.label }}</span>
                <strong class="metric-mono">{{ item.value }}</strong>
              </div>
            </div>
          </div>

          <div class="floating-panel floating-panel-primary">
            <span>Focus Window</span>
            <strong class="metric-mono">4.6h</strong>
            <p>深度工作时间保持稳定。</p>
          </div>

          <div class="floating-panel floating-panel-secondary">
            <span>Community Signal</span>
            <strong class="metric-mono">+12</strong>
            <p>有新的高质量反馈可跟进。</p>
          </div>
        </div>
      </section>

      <section class="login-card">
        <div class="card-glow-line"></div>

        <div class="login-header">
          <p class="panel-tag">Welcome Back</p>
          <h2>登录账号</h2>
          <p>继续你的学习与项目协作进度。</p>
        </div>

        <div class="login-badges">
          <span v-for="badge in loginBadges" :key="badge" class="login-badge">{{ badge }}</span>
        </div>

        <div class="system-status-strip">
          <article v-for="status in systemStatus" :key="status.label" class="status-item">
            <span class="status-dot" :class="status.tone"></span>
            <div>
              <strong>{{ status.label }}</strong>
              <p>{{ status.detail }}</p>
            </div>
          </article>
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

            <div class="login-note">
              <span class="login-note-title">Workspace Access</span>
              <p>登录后即可进入统一工作台，继续项目、课程与社区协作的上下文。</p>
            </div>
          </div>
        </el-form>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import { ParticlesComponent as Particles } from 'particles.vue3'
import { loadSlim } from '@tsparticles/slim'
import { tsParticles } from '@tsparticles/engine'
import type { FormInstance, FormRules } from 'element-plus'

const platformMetrics = [
  { label: '进行中项目', value: '06', detail: '当前冲刺保持稳定推进' },
  { label: '学习进度', value: '72%', detail: 'LangChain 路线持续完成' },
  { label: '社区反馈', value: '12', detail: '最新讨论可直接跟进' }
]

const platformFeatures = [
  '项目仪表板与阶段进度跟踪',
  '学习路线、知识地图与资料导航',
  '代码示例、实验记录与部署入口',
  '社区问答与高质量反馈整合'
]

const workspaceFlow = [
  { step: '01', title: 'Sprint Review', detail: '聚焦项目冲刺、风险点和当日优先级。' },
  { step: '02', title: 'Learning Route', detail: '延续 LangChain 学习路径和阶段进度。' },
  { step: '03', title: 'Deploy Check', detail: '统一查看实验、部署和社区反馈信号。' }
]

const previewSignals = [
  { label: 'Run Count', value: '128' },
  { label: 'Progress', value: '84%' },
  { label: 'Active Tasks', value: '09' }
]

const loginBadges = ['Unified workspace', 'Dark glass UI', 'Fast demo access']

const systemStatus = [
  { label: 'Project Sync', detail: '冲刺与进度状态已同步', tone: 'is-primary' },
  { label: 'Learning Context', detail: '学习路线可从上次位置继续', tone: 'is-secondary' },
  { label: 'Access Ready', detail: '演示账号可直接快速进入', tone: 'is-success' }
]

const particlesOptions = {
  background: {
    color: { value: 'transparent' }
  },
  fpsLimit: 60,
  particles: {
    number: {
      value: 28,
      density: {
        enable: true,
        area: 1100
      }
    },
    color: {
      value: ['#3b82f6', '#06b6d4', '#8b5cf6']
    },
    links: {
      enable: true,
      distance: 160,
      color: '#3b82f6',
      opacity: 0.06,
      width: 1
    },
    opacity: {
      value: { min: 0.06, max: 0.18 }
    },
    move: {
      enable: true,
      speed: 0.28,
      random: true,
      outModes: {
        default: 'out'
      }
    },
    size: {
      value: { min: 1, max: 2.2 }
    }
  },
  interactivity: {
    events: {
      onHover: {
        enable: true,
        mode: 'grab'
      },
      resize: true
    },
    modes: {
      grab: {
        distance: 120,
        links: {
          opacity: 0.14
        }
      }
    }
  },
  detectRetina: true
}

loadSlim(tsParticles)

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
  padding: clamp(24px, 4vw, 40px);
  position: relative;
  overflow: hidden;
}

.particles-layer {
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  opacity: 0.88;
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
  width: min(1160px, 100%);
  display: grid;
  grid-template-columns: minmax(0, 1.1fr) minmax(360px, 420px);
  gap: clamp(24px, 4vw, 48px);
  align-items: center;
  position: relative;
  z-index: 1;
}

.brand-panel {
  display: grid;
  gap: 28px;
  padding: clamp(8px, 2vw, 20px);
}

.brand-headline,
.login-title,
.login-subtitle,
.brand-metrics,
.brand-feature-panel,
.workspace-preview,
.card-glow-line,
.login-header,
.login-badges,
.system-status-strip,
.login-form {
  opacity: 0;
  animation: lift-in 780ms cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
}

.brand-headline {
  animation-delay: 80ms;
}

.login-title {
  animation-delay: 140ms;
}

.login-subtitle {
  animation-delay: 220ms;
}

.brand-metrics {
  animation-delay: 300ms;
}

.brand-feature-panel {
  animation-delay: 380ms;
}

.workspace-preview {
  animation-delay: 460ms;
}

.card-glow-line {
  animation-delay: 180ms;
}

.login-header {
  animation-delay: 240ms;
}

.login-badges {
  animation-delay: 320ms;
}

.system-status-strip {
  animation-delay: 400ms;
}

.login-form {
  animation-delay: 480ms;
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

.brand-status {
  color: var(--text-secondary);
  font-size: 13px;
}

.login-eyebrow,
.feature-panel-label,
.panel-tag,
.metric-card p,
.quick-login-label,
.demo-account span,
.login-note-title,
.preview-signal span {
  margin: 0;
  color: var(--color-secondary);
  font-size: 11px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
}

.login-title {
  margin: 0;
  font-size: clamp(42px, 7vw, 72px);
  line-height: 0.96;
  max-width: 10ch;
}

.login-subtitle {
  margin: 0;
  max-width: 680px;
  color: var(--text-secondary);
  font-size: 17px;
  line-height: 1.8;
}

.brand-metrics {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}

.metric-card,
.brand-feature-panel,
.login-card {
  @include section-shell;
}

.metric-card {
  padding: 18px;
  display: grid;
  gap: 10px;
  position: relative;
  overflow: hidden;
}

.metric-card strong {
  font-size: clamp(28px, 4vw, 36px);
  line-height: 1;
}

.metric-card::after {
  content: '';
  position: absolute;
  inset: auto -20% -55% auto;
  width: 120px;
  height: 120px;
  border-radius: 999px;
  background: radial-gradient(circle, rgba(59, 130, 246, 0.16), transparent 72%);
}

.metric-card span {
  color: var(--text-secondary);
  line-height: 1.6;
}

.brand-feature-panel {
  padding: 24px;
  background: rgba(255, 255, 255, 0.04);
}

.workspace-preview {
  position: relative;
  min-height: 300px;
  padding: 28px 18px 22px;
}

.preview-orbit {
  position: absolute;
  inset: 10px auto auto -6px;
  width: 210px;
  height: 210px;
  pointer-events: none;
  opacity: 0.78;
}

.orbit-ring {
  position: absolute;
  inset: 0;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.07);
}

.orbit-ring-outer {
  animation: orbit-spin 18s linear infinite;
}

.orbit-ring-inner {
  inset: 28px;
  border-color: rgba(6, 182, 212, 0.16);
  animation: orbit-spin-reverse 12s linear infinite;
}

.orbit-ring-outer::before,
.orbit-ring-inner::before {
  content: '';
  position: absolute;
  top: -4px;
  left: 50%;
  width: 8px;
  height: 8px;
  border-radius: 999px;
  transform: translateX(-50%);
  background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
  box-shadow: 0 0 18px rgba(59, 130, 246, 0.42);
}

.orbit-node {
  position: absolute;
  width: 12px;
  height: 12px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.88);
  box-shadow: 0 0 18px rgba(255, 255, 255, 0.4);
}

.orbit-node-one {
  right: 24px;
  top: 34px;
  animation: node-pulse 3.8s ease-in-out infinite;
}

.orbit-node-two {
  left: 34px;
  bottom: 24px;
  width: 9px;
  height: 9px;
  background: rgba(6, 182, 212, 0.9);
  box-shadow: 0 0 18px rgba(6, 182, 212, 0.42);
  animation: node-pulse 4.6s ease-in-out infinite;
  animation-delay: -1.4s;
}

.preview-surface {
  @include section-shell;
  padding: 24px;
  min-height: 272px;
  position: relative;
  overflow: hidden;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.07), rgba(255, 255, 255, 0.03)),
    rgba(255, 255, 255, 0.03);
}

.preview-surface::before {
  content: '';
  position: absolute;
  inset: 0;
  background:
    linear-gradient(120deg, transparent 20%, rgba(255, 255, 255, 0.08) 48%, transparent 76%);
  transform: translateX(-120%);
  animation: surface-sheen 10s linear infinite;
}

.preview-surface::after {
  content: '';
  position: absolute;
  inset: auto 0 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(6, 182, 212, 0.4), transparent);
}

.preview-header {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: flex-start;
}

.preview-header strong {
  display: block;
  margin-top: 8px;
  font-size: 20px;
}

.preview-badge {
  padding: 8px 12px;
  border-radius: 999px;
  color: var(--text-primary);
  font-size: 12px;
  background: rgba(34, 197, 94, 0.14);
  border: 1px solid rgba(34, 197, 94, 0.24);
}

.preview-flow {
  margin-top: 24px;
  display: grid;
  gap: 14px;
}

.preview-flow-item {
  @include panel-hover;
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 14px;
  padding: 14px 16px;
  border-radius: 18px;
  border: 1px solid var(--line-soft);
  background: rgba(255, 255, 255, 0.03);
}

.preview-flow-item:nth-child(1) {
  animation: card-breathe 6s ease-in-out infinite;
}

.preview-flow-item:nth-child(2) {
  animation: card-breathe 6s ease-in-out infinite;
  animation-delay: -2s;
}

.preview-flow-item:nth-child(3) {
  animation: card-breathe 6s ease-in-out infinite;
  animation-delay: -4s;
}

.preview-step-index {
  width: 44px;
  height: 44px;
  border-radius: 14px;
  display: grid;
  place-items: center;
  color: var(--text-primary);
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.32), rgba(139, 92, 246, 0.28));
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.preview-flow-item strong,
.preview-flow-item p {
  margin: 0;
}

.preview-flow-item p {
  margin-top: 6px;
  color: var(--text-secondary);
  line-height: 1.6;
}

.preview-footer {
  margin-top: 18px;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}

.preview-signal {
  @include panel-hover;
  padding: 14px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--line-soft);
  display: grid;
  gap: 8px;
}

.preview-signal:nth-child(2) {
  animation: signal-glow 5.5s ease-in-out infinite;
}

.preview-signal strong {
  font-size: 18px;
}

.floating-panel {
  position: absolute;
  min-width: 180px;
  padding: 14px 16px;
  border-radius: 18px;
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 20px 40px rgba(6, 9, 16, 0.28);
  animation: panel-float 7s ease-in-out infinite;
}

.floating-panel span,
.floating-panel p,
.floating-panel strong {
  display: block;
  margin: 0;
}

.floating-panel strong {
  margin-top: 6px;
  font-size: 26px;
}

.floating-panel p {
  margin-top: 4px;
  color: var(--text-secondary);
  line-height: 1.5;
}

.floating-panel-primary {
  top: 0;
  right: -12px;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.18), rgba(6, 182, 212, 0.08));
}

.floating-panel-secondary {
  left: 8px;
  bottom: -6px;
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.16), rgba(255, 255, 255, 0.05));
  animation-delay: -3s;
}

.feature-list {
  list-style: none;
  margin: 18px 0 0;
  padding: 0;
  display: grid;
  gap: 14px;
}

.feature-list li {
  position: relative;
  padding-left: 18px;
  color: var(--text-secondary);
  line-height: 1.7;
}

.feature-list li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 11px;
  width: 8px;
  height: 8px;
  border-radius: 999px;
  background: linear-gradient(135deg, var(--color-secondary), var(--color-accent));
  box-shadow: 0 0 0 4px rgba(6, 182, 212, 0.12);
}

.login-card {
  padding: clamp(28px, 4vw, 36px);
  background: rgba(255, 255, 255, 0.06);
  border-radius: var(--radius-xl);
  position: relative;
  overflow: hidden;
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
  margin-bottom: 22px;
  background: linear-gradient(90deg, var(--color-primary), var(--color-secondary), var(--color-accent));
  box-shadow: 0 0 26px rgba(59, 130, 246, 0.3);
}

.login-header {
  display: grid;
  gap: 10px;
  margin-bottom: 24px;
}

.login-header h2 {
  margin: 0;
  font-size: clamp(28px, 4vw, 36px);
  color: var(--text-primary);
}

.login-header p:last-child {
  margin: 0;
  color: var(--text-secondary);
  line-height: 1.7;
}

.login-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 18px;
}

.login-badge {
  position: relative;
  padding: 8px 12px;
  padding-left: 26px;
  border-radius: 999px;
  border: 1px solid var(--line-soft);
  background: rgba(255, 255, 255, 0.04);
  color: var(--text-secondary);
  font-size: 12px;
}

.login-badge::before {
  content: '';
  position: absolute;
  left: 12px;
  top: 50%;
  width: 7px;
  height: 7px;
  border-radius: 999px;
  transform: translateY(-50%);
  background: linear-gradient(135deg, var(--color-secondary), var(--color-accent));
  box-shadow: 0 0 12px rgba(59, 130, 246, 0.3);
}

.system-status-strip {
  display: grid;
  gap: 10px;
  margin-bottom: 20px;
}

.status-item {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 12px;
  padding: 12px 14px;
  border-radius: 16px;
  border: 1px solid var(--line-soft);
  background: rgba(255, 255, 255, 0.03);
}

.status-item:hover .status-dot {
  transform: scale(1.12);
  box-shadow: 0 0 0 6px rgba(255, 255, 255, 0.04);
}

.status-item strong,
.status-item p {
  margin: 0;
}

.status-item strong {
  font-size: 13px;
  color: var(--text-primary);
}

.status-item p {
  margin-top: 4px;
  color: var(--text-secondary);
  font-size: 13px;
  line-height: 1.6;
}

.status-dot {
  width: 10px;
  height: 10px;
  margin-top: 5px;
  border-radius: 999px;
  box-shadow: 0 0 0 5px rgba(255, 255, 255, 0.03);
  transition: transform var(--transition-base), box-shadow var(--transition-base);
}

.status-dot.is-primary {
  background: var(--color-primary);
}

.status-dot.is-secondary {
  background: var(--color-secondary);
}

.status-dot.is-success {
  background: var(--color-success);
}

.login-form {
  display: grid;
  gap: 8px;
}

.login-form :deep(.el-form-item) {
  margin-bottom: 12px;
}

.login-form :deep(.el-input__wrapper) {
  min-height: 50px;
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
  min-height: 50px;
  margin-top: 4px;
  border: none;
  border-radius: 14px;
  font-size: 15px;
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
  margin-top: 22px;
  padding-top: 22px;
  border-top: 1px solid var(--line-soft);
  display: grid;
  gap: 18px;
}

.demo-account {
  display: grid;
  gap: 8px;
}

.demo-account strong {
  color: var(--text-primary);
  font-size: 15px;
}

.quick-login {
  display: grid;
  gap: 12px;
}

.login-note {
  padding: 14px 16px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--line-soft);
}

.login-note p {
  margin: 8px 0 0;
  color: var(--text-secondary);
  line-height: 1.7;
}

.quick-login-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.quick-login-chip {
  @include panel-hover;
  display: inline-flex;
  align-items: center;
  padding: 10px 14px;
  border-radius: 999px;
  border: 1px solid var(--line-soft);
  background: rgba(255, 255, 255, 0.04);
  color: var(--text-primary);
  cursor: pointer;
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

@keyframes lift-in {
  from {
    opacity: 0;
    transform: translateY(26px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
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

@keyframes orbit-spin {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}

@keyframes orbit-spin-reverse {
  from {
    transform: rotate(360deg);
  }

  to {
    transform: rotate(0deg);
  }
}

@keyframes node-pulse {
  0%,
  100% {
    transform: scale(1);
    opacity: 0.8;
  }

  50% {
    transform: scale(1.22);
    opacity: 1;
  }
}

@keyframes surface-sheen {
  0% {
    transform: translateX(-140%);
  }

  100% {
    transform: translateX(140%);
  }
}

@keyframes card-breathe {
  0%,
  100% {
    transform: translateY(0);
  }

  50% {
    transform: translateY(-3px);
  }
}

@keyframes panel-float {
  0%,
  100% {
    transform: translateY(0);
  }

  50% {
    transform: translateY(-8px);
  }
}

@keyframes signal-glow {
  0%,
  100% {
    box-shadow: none;
    border-color: var(--line-soft);
  }

  50% {
    box-shadow: 0 0 0 1px rgba(6, 182, 212, 0.14), 0 14px 32px rgba(6, 182, 212, 0.08);
    border-color: rgba(6, 182, 212, 0.24);
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
  }

  .login-title {
    max-width: none;
  }

  .workspace-preview {
    padding-inline: 0;
  }

  .floating-panel-primary {
    right: 0;
  }

  .ambient-orb {
    width: 320px;
    height: 320px;
  }

  .preview-orbit {
    inset: 8px auto auto 0;
    width: 170px;
    height: 170px;
  }
}

@media (max-width: 640px) {
  .login-container {
    padding: 18px;
  }

  .brand-metrics {
    grid-template-columns: 1fr;
  }

  .login-shell {
    grid-template-columns: 1fr;
  }

  .login-card {
    min-width: 0;
  }

  .brand-headline,
  .preview-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .preview-footer {
    grid-template-columns: 1fr;
  }

  .floating-panel {
    position: static;
    margin-top: 14px;
  }

  .preview-orbit {
    display: none;
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
}

@media (prefers-reduced-motion: reduce) {
  .brand-headline,
  .login-title,
  .login-subtitle,
  .brand-metrics,
  .brand-feature-panel,
  .workspace-preview,
  .card-glow-line,
  .login-header,
  .login-badges,
  .system-status-strip,
  .login-form {
    opacity: 1;
    animation: none;
  }

  .ambient-orb,
  .brand-mark,
  .orbit-ring,
  .orbit-node,
  .preview-surface::before,
  .preview-flow-item,
  .preview-signal,
  .floating-panel,
  .login-button::after {
    animation: none;
  }
}
</style>