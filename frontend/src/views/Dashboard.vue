<template>
  <div class="dashboard">
    <!-- 粒子特效背景 -->
    <Particles
      id="tsparticles"
      :options="particlesOptions as any"
      @particles-loaded="particlesLoaded"
      class="particles-background"
    />
    
    <!-- 页面头部 -->
    <div class="dashboard-header">
      <h1 class="dashboard-title">Agent Learning Platform</h1>
      <p class="dashboard-subtitle">AI Agent学习平台 - 仪表板</p>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-grid">
      <el-card class="stat-card" shadow="hover">
        <div class="stat-content">
          <div class="stat-icon">
            <el-icon size="24" color="#409eff">
              <FolderOpened />
            </el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">12</div>
            <div class="stat-label">进行中的项目</div>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card" shadow="hover">
        <div class="stat-content">
          <div class="stat-icon">
            <el-icon size="24" color="#67c23a">
              <Reading />
            </el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">8</div>
            <div class="stat-label">学习教程</div>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card" shadow="hover">
        <div class="stat-content">
          <div class="stat-icon">
            <el-icon size="24" color="#e6a23c">
              <User />
            </el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">156</div>
            <div class="stat-label">社区成员</div>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card" shadow="hover">
        <div class="stat-content">
          <div class="stat-icon">
            <el-icon size="24" color="#f56c6c">
              <Clock />
            </el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">48</div>
            <div class="stat-label">小时学习时间</div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 新布局：第一行2个大模块 + 第二行4个小模块 -->
    <div class="new-layout">
      <!-- 第一行：2个大模块（项目进度 + 系统通知）各占1/2宽度 -->
      <div class="top-row">
        <!-- 大模块1：项目进度 -->
        <el-card class="large-module" shadow="never">
          <template #header>
            <div class="card-header">
              <h3>
                <el-icon><TrendCharts /></el-icon>
                项目进度
              </h3>
              <el-button type="primary" link>查看全部</el-button>
            </div>
          </template>
          
          <div class="project-list">
            <div v-for="project in projects" :key="project.id" class="project-item">
              <div class="project-info">
                <div class="project-name">{{ project.name }}</div>
                <div class="project-description">{{ project.description }}</div>
                <div class="project-meta">
                  <span class="meta-item">
                    <el-icon><Calendar /></el-icon>
                    {{ project.dueDate }}
                  </span>
                  <span class="meta-item">
                    <el-icon><User /></el-icon>
                    {{ project.members }}人
                  </span>
                </div>
              </div>
              <div class="project-progress">
                <el-progress 
                  :percentage="project.progress" 
                  :status="project.status"
                  :stroke-width="8"
                />
                <div class="progress-label">{{ project.progress }}% 完成</div>
              </div>
            </div>
          </div>
        </el-card>

        <!-- 大模块2：系统通知 -->
        <el-card class="large-module" shadow="never">
          <template #header>
            <div class="card-header">
              <h3>
                <el-icon><Notification /></el-icon>
                系统通知
              </h3>
              <el-button type="primary" link @click="markAllAsRead">全部标记已读</el-button>
            </div>
          </template>
          
          <div class="notification-list">
            <div v-for="notification in notifications" :key="notification.id" 
                 :class="['notification-item', { unread: !notification.read }]">
              <div class="notification-icon">
                <el-icon :color="notification.color">
                  <component :is="notification.icon" />
                </el-icon>
              </div>
              <div class="notification-content">
                <div class="notification-title">{{ notification.title }}</div>
                <div class="notification-message">{{ notification.message }}</div>
                <div class="notification-time">{{ notification.time }}</div>
              </div>
              <div class="notification-actions">
                <el-button v-if="!notification.read" type="text" size="small" @click="markAsRead(notification.id)">
                  标记已读
                </el-button>
              </div>
            </div>
          </div>
        </el-card>
      </div>

      <!-- 第二行：4个小模块各占1/4宽度 -->
      <div class="bottom-row">
        <!-- 小模块1：社区交流 -->
        <el-card class="small-module" shadow="never">
          <template #header>
            <div class="card-header">
              <h3>
                <el-icon><Promotion /></el-icon>
                社区交流
              </h3>
              <el-button type="primary" link>进入社区</el-button>
            </div>
          </template>
          
          <div class="community-list">
            <div v-for="community in communities" :key="community.id" class="community-item">
              <div class="community-icon">
                <el-icon :color="community.color">
                  <component :is="community.icon" />
                </el-icon>
              </div>
              <div class="community-content">
                <div class="community-title">{{ community.title }}</div>
                <div class="community-meta">
                  <span class="meta-item">
                    <el-icon><User /></el-icon>
                    {{ community.members }}
                  </span>
                  <span class="meta-item">
                    <el-icon><ChatDotRound /></el-icon>
                    {{ community.posts }}
                  </span>
                </div>
                <div class="community-description">{{ community.description }}</div>
              </div>
              <el-button type="primary" size="small" class="join-button">加入</el-button>
            </div>
          </div>
        </el-card>

        <!-- 小模块2：学习活动 -->
        <el-card class="small-module" shadow="never">
          <template #header>
            <div class="card-header">
              <h3>
                <el-icon><Connection /></el-icon>
                学习活动
              </h3>
              <el-button type="primary" link>历史记录</el-button>
            </div>
          </template>
          
          <div class="activity-list">
            <div v-for="activity in activities" :key="activity.id" class="activity-item">
              <div class="activity-icon">
                <el-icon :color="activity.color">
                  <component :is="activity.icon" />
                </el-icon>
              </div>
              <div class="activity-content">
                <div class="activity-title">{{ activity.title }}</div>
                <div class="activity-description">{{ activity.description }}</div>
                <div class="activity-time">{{ activity.time }}</div>
              </div>
            </div>
          </div>
        </el-card>

        <!-- 小模块3：快速操作 -->
        <el-card class="small-module" shadow="never">
          <template #header>
            <div class="card-header">
              <h3>
                <el-icon><Operation /></el-icon>
                快速操作
              </h3>
              <el-button type="text" size="small">查看更多</el-button>
            </div>
          </template>
          
          <div class="quick-actions">
            <div 
              v-for="action in quickActions" 
              :key="action.id"
              class="action-item"
              :class="`action-${action.type}`"
              @click="handleAction(action.action)"
            >
              <div class="action-icon">
                <el-icon>
                  <component :is="action.icon" />
                </el-icon>
              </div>
              <div class="action-content">
                <div class="action-label">{{ action.label }}</div>
                <div class="action-desc">{{ getActionDesc(action.action) }}</div>
              </div>
            </div>
          </div>
        </el-card>

        <!-- 小模块4：技术栈 -->
        <el-card class="small-module" shadow="never">
          <template #header>
            <div class="card-header">
              <h3>
                <el-icon><Grid /></el-icon>
                技术栈
              </h3>
            </div>
          </template>
          
          <div class="tech-stack">
            <div v-for="tech in techStack" :key="tech.name" class="tech-item">
              <div class="tech-icon">
                <img :src="tech.icon" :alt="tech.name" />
              </div>
              <div class="tech-info">
                <div class="tech-name">{{ tech.name }}</div>
                <div class="tech-version">{{ tech.version }}</div>
              </div>
              <el-tag :type="tech.status" size="small">{{ tech.statusText }}</el-tag>
            </div>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import {
  FolderOpened,
  Reading,
  User,
  Clock,
  Calendar,
  Document,
  VideoPlay,
  ChatDotRound,
  Bell,
  Warning,
  SuccessFilled,
  InfoFilled,
  Setting,
  TrendCharts,
  Notification,
  Promotion,
  Connection,
  Operation,
  Grid
  // ArrowRight, // 暂时注释掉未使用的导入
  // HelpFilled, // 暂时注释掉未使用的导入
  // Monitor, // 暂时注释掉未使用的导入
} from '@element-plus/icons-vue'
// import type { Action } from 'element-plus' // 暂时注释掉未使用的导入
// 使用 particles.vue3 的 ParticlesComponent
import { ParticlesComponent as Particles } from 'particles.vue3'
import { loadSlim } from '@tsparticles/slim'
import { tsParticles } from '@tsparticles/engine'

// 项目数据
const projects = ref([
  {
    id: 1,
    name: '智能文档助手',
    description: '基于LangChain的文档问答系统',
    dueDate: '2026-04-30',
    members: 3,
    progress: 75,
    status: 'success'
  },
  {
    id: 2,
    name: '代码审查Agent',
    description: '自动化代码审查工具',
    dueDate: '2026-05-15',
    members: 2,
    progress: 45,
    status: 'warning'
  },
  {
    id: 3,
    name: '学习进度跟踪',
    description: '个人学习管理系统',
    dueDate: '2026-04-25',
    members: 1,
    progress: 90,
    status: 'success'
  }
])

// 学习活动数据
const activities = ref([
  {
    id: 1,
    icon: Document,
    color: '#409eff',
    title: '完成Vue 3基础教程',
    description: '学习了Composition API和响应式系统',
    time: '2小时前'
  },
  {
    id: 2,
    icon: VideoPlay,
    color: '#67c23a',
    title: '观看LangChain实战视频',
    description: '掌握了Chain和Agent的基本用法',
    time: '5小时前'
  },
  {
    id: 3,
    icon: ChatDotRound,
    color: '#e6a23c',
    title: '参与社区讨论',
    description: '在BotLearn社区回答了3个问题',
    time: '昨天'
  }
])

// 快速操作
const quickActions = ref([
  {
    id: 1,
    label: '新建项目',
    icon: FolderOpened,
    type: 'primary',
    action: 'createProject'
  },
  {
    id: 2,
    label: '开始学习',
    icon: Reading,
    type: 'success',
    action: 'startLearning'
  },
  {
    id: 3,
    label: '社区交流',
    icon: ChatDotRound,
    type: 'info',
    action: 'communityChat'
  },
  {
    id: 4,
    label: '系统设置',
    icon: Setting,
    type: 'warning',
    action: 'systemSettings'
  }
])

// 获取操作描述
const getActionDesc = (action: string) => {
  const descMap: Record<string, string> = {
    createProject: '创建新的AI Agent项目',
    startLearning: '开始学习AI Agent技术',
    communityChat: '与开发者交流技术',
    systemSettings: '配置平台参数'
  }
  return descMap[action] || '执行操作'
}

// 粒子特效配置
const particlesOptions = {
  background: {
    color: {
      value: 'transparent'
    }
  },
  fpsLimit: 120,
  interactivity: {
    events: {
      onClick: {
        enable: true,
        mode: 'push'
      },
      onHover: {
        enable: true,
        mode: 'repulse'
      },
      resize: true
    },
    modes: {
      push: {
        quantity: 4
      },
      repulse: {
        distance: 100,
        duration: 0.4
      }
    }
  },
  particles: {
    color: {
      value: ['#3b82f6', '#8b5cf6', '#60a5fa', '#a78bfa'] // 主题色系
    },
    links: {
      color: '#3b82f6',
      distance: 150,
      enable: true,
      opacity: 0.3,
      width: 1
    },
    move: {
      direction: 'none',
      enable: true,
      outModes: {
        default: 'bounce'
      },
      random: false,
      speed: 1,
      straight: false
    },
    number: {
      density: {
        enable: true,
        area: 800
      },
      value: 60
    },
    opacity: {
      value: 0.5
    },
    shape: {
      type: 'circle'
    },
    size: {
      value: { min: 1, max: 3 }
    }
  },
  detectRetina: true
}

// 加载粒子引擎
loadSlim(tsParticles)

const particlesLoaded = async (container: any) => {
  console.log('Particles container loaded', container)
}

// 通知数据
const notifications = ref([
  {
    id: 1,
    icon: Bell,
    color: '#409eff',
    title: '新版本发布',
    message: 'Agent Learning Platform v1.0.0 已发布',
    time: '10分钟前',
    read: false
  },
  {
    id: 2,
    icon: SuccessFilled,
    color: '#67c23a',
    title: '项目完成',
    message: '智能文档助手项目进度达到100%',
    time: '1小时前',
    read: true
  },
  {
    id: 3,
    icon: Warning,
    color: '#e6a23c',
    title: '系统维护',
    message: '本周六凌晨2:00-4:00进行系统维护',
    time: '3小时前',
    read: false
  },
  {
    id: 4,
    icon: InfoFilled,
    color: '#909399',
    title: '社区活动',
    message: 'BotLearn技术分享会将于本周五举行',
    time: '昨天',
    read: true
  }
])

// 社区交流数据
const communities = ref([
  {
    id: 1,
    icon: ChatDotRound,
    color: '#409eff',
    title: 'BotLearn技术社区',
    description: 'AI Agent技术讨论与分享',
    members: '1.2k',
    posts: '356'
  },
  {
    id: 2,
    icon: 'Promotion',
    color: '#67c23a',
    title: 'Vue 3开发组',
    description: 'Vue 3最佳实践与源码解析',
    members: '856',
    posts: '189'
  },
  {
    id: 3,
    icon: 'Connection',
    color: '#e6a23c',
    title: 'OpenClaw开发者',
    description: 'OpenClaw技能开发与集成',
    members: '432',
    posts: '124'
  },
  {
    id: 4,
    icon: 'HelpFilled',
    color: '#f56c6c',
    title: '新手问答区',
    description: '新手问题解答与学习指导',
    members: '2.3k',
    posts: '567'
  }
])

// 技术栈数据
const techStack = ref([
  {
    name: 'Vue 3',
    version: '3.4.0',
    icon: 'https://vuejs.org/logo.svg',
    status: 'success',
    statusText: '活跃'
  },
  {
    name: 'TypeScript',
    version: '5.3.0',
    icon: 'https://www.typescriptlang.org/favicon-32x32.png',
    status: 'success',
    statusText: '活跃'
  },
  {
    name: 'FastAPI',
    version: '0.104.0',
    icon: 'https://fastapi.tiangolo.com/img/favicon.png',
    status: 'warning',
    statusText: '开发中'
  },
  {
    name: 'LangChain',
    version: '0.1.0',
    icon: 'https://python.langchain.com/img/favicon.ico',
    status: 'warning',
    statusText: '集成中'
  }
])

// 操作方法
const handleAction = (action: string) => {
  console.log('执行操作:', action)
  // 这里可以添加具体的操作逻辑
}

const markAsRead = (id: number) => {
  const notification = notifications.value.find(n => n.id === id)
  if (notification) {
    notification.read = true
  }
}

const markAllAsRead = () => {
  notifications.value.forEach(notification => {
    notification.read = true
  })
}
</script>

<style scoped>
/* 有机自然风仪表板 */
.dashboard {
  padding: 20px;
  min-height: calc(100vh - 72px); /* 减去导航栏高度 */
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  position: relative;
  overflow-x: hidden;
}

/* 文化科技风 - 渐变背景特效 */
.dashboard::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 10% 20%, rgba(59, 130, 246, 0.08) 0%, transparent 40%),
    radial-gradient(circle at 90% 80%, rgba(139, 92, 246, 0.08) 0%, transparent 40%),
    radial-gradient(circle at 50% 50%, rgba(99, 102, 241, 0.05) 0%, transparent 60%);
  pointer-events: none;
  z-index: 0;
  animation: gradientShift 20s ease infinite alternate;
}

@keyframes gradientShift {
  0% {
    background: 
      radial-gradient(circle at 10% 20%, rgba(59, 130, 246, 0.08) 0%, transparent 40%),
      radial-gradient(circle at 90% 80%, rgba(139, 92, 246, 0.08) 0%, transparent 40%),
      radial-gradient(circle at 50% 50%, rgba(99, 102, 241, 0.05) 0%, transparent 60%);
  }
  50% {
    background: 
      radial-gradient(circle at 90% 20%, rgba(59, 130, 246, 0.08) 0%, transparent 40%),
      radial-gradient(circle at 10% 80%, rgba(139, 92, 246, 0.08) 0%, transparent 40%),
      radial-gradient(circle at 50% 50%, rgba(99, 102, 241, 0.05) 0%, transparent 60%);
  }
  100% {
    background: 
      radial-gradient(circle at 50% 20%, rgba(59, 130, 246, 0.08) 0%, transparent 40%),
      radial-gradient(circle at 50% 80%, rgba(139, 92, 246, 0.08) 0%, transparent 40%),
      radial-gradient(circle at 50% 50%, rgba(99, 102, 241, 0.05) 0%, transparent 60%);
  }
}

/* 粒子特效容器 */
.particles-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 0;
  pointer-events: none;
}

/* 确保内容在粒子之上 */
.dashboard > *:not(.particles-background) {
  position: relative;
  z-index: 1;
}

.dashboard > * {
  position: relative;
  z-index: 1;
}

/* 文化科技风 - 页面标题增强 */
.dashboard-header {
  margin-bottom: 24px;
  text-align: center;
  position: relative;
}

.dashboard-title {
  font-size: 36px;
  font-weight: 800;
  margin-bottom: 8px;
  background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #3b82f6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  background-size: 200% 100%;
  letter-spacing: -0.5px;
  position: relative;
  display: inline-block;
  animation: titleShine 3s ease-in-out infinite;
}

@keyframes titleShine {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

.dashboard-title::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  width: 120px;
  height: 3px;
  background: linear-gradient(90deg, transparent, #3b82f6, #8b5cf6, transparent);
  border-radius: 2px;
  animation: lineFlow 2s ease-in-out infinite;
}

@keyframes lineFlow {
  0%, 100% {
    background: linear-gradient(90deg, transparent, #3b82f6, #8b5cf6, transparent);
  }
  50% {
    background: linear-gradient(90deg, transparent, #8b5cf6, #3b82f6, transparent);
  }
}

.dashboard-subtitle {
  font-size: 16px;
  color: #64748b;
  font-weight: 400;
  letter-spacing: 1px;
  margin-top: 8px;
  position: relative;
  display: inline-block;
}

.dashboard-subtitle::before,
.dashboard-subtitle::after {
  content: '✦';
  color: #3b82f6;
  margin: 0 12px;
  font-size: 14px;
  animation: starTwinkle 2s ease-in-out infinite;
}

@keyframes starTwinkle {
  0%, 100% {
    opacity: 0.7;
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(1.2);
  }
}

.dashboard-header {
  margin-bottom: 40px;
  text-align: center;
  position: relative;
}

.dashboard-title {
  font-size: 42px;
  font-weight: 800;
  margin-bottom: 12px;
  background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 50%, #f472b6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.5px;
  position: relative;
  display: inline-block;
}

.dashboard-title::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  width: 120px;
  height: 3px;
  background: linear-gradient(90deg, transparent, #60a5fa, transparent);
  border-radius: 2px;
}

.dashboard-subtitle {
  font-size: 18px;
  color: #94a3b8;
  font-weight: 300;
  letter-spacing: 1px;
  text-transform: uppercase;
  margin-top: 16px;
}

/* 有机自然风统计卡片 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  border-radius: 14px;
  border: none;
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(226, 232, 240, 0.8);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 4px 12px rgba(0, 0, 0, 0.04),
    0 1px 2px rgba(0, 0, 0, 0.02);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

/* 打破规整感 - 每个卡片不同圆角 */
.stat-card:nth-child(1) {
  border-radius: 16px 14px 14px 16px;
}

.stat-card:nth-child(2) {
  border-radius: 14px 16px 16px 14px;
}

.stat-card:nth-child(3) {
  border-radius: 14px 16px 14px 16px;
}

.stat-card:nth-child(4) {
  border-radius: 16px 14px 16px 14px;
}

/* 自然装饰条 */
.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #3b82f6, #8b5cf6);
  opacity: 0.7;
  transition: opacity 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 
    0 12px 32px rgba(0, 0, 0, 0.08),
    0 4px 12px rgba(59, 130, 246, 0.1);
  border-color: rgba(59, 130, 246, 0.3);
  background: white;
}

.stat-card:hover::before {
  opacity: 1;
  height: 4px;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 
    0 12px 24px rgba(59, 130, 246, 0.1),
    0 0 0 1px rgba(59, 130, 246, 0.2);
  border-color: rgba(59, 130, 246, 0.3);
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 24px;
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(139, 92, 246, 0.1));
  border: 1px solid rgba(59, 130, 246, 0.2);
  position: relative;
  overflow: hidden;
}

.stat-icon :deep(.el-icon) {
  font-size: 24px;
  width: 24px;
  height: 24px;
}

.stat-icon::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, transparent, rgba(59, 130, 246, 0.1), transparent);
  transform: translateX(-100%);
  transition: transform 0.6s ease;
}

.stat-card:hover .stat-icon::before {
  transform: translateX(100%);
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 36px;
  font-weight: 800;
  color: #1a1a1a;
  line-height: 1;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -1px;
}

.stat-label {
  font-size: 14px;
  color: #64748b;
  margin-top: 6px;
  font-weight: 500;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

/* 新布局：第一行2个大模块 + 第二行4个小模块 */
.new-layout {
  display: flex;
  flex-direction: column;
  gap: 20px;
  animation: fadeInUp 0.6s ease-out;
  position: relative;
  z-index: 1;
}

/* 第一行：2个大模块各占1/2宽度 */
.top-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  min-height: 300px; /* 恢复原高度，只是header压缩了 */
}

.large-module {
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(226, 232, 240, 0.8);
  overflow: hidden;
  transition: all 0.3s ease;
  position: relative;
  box-shadow: 
    0 4px 12px rgba(0, 0, 0, 0.04),
    0 1px 2px rgba(0, 0, 0, 0.02);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  min-height: 300px; /* 整体卡片高度不变 */
  display: block !important; /* 强制block布局，避免flex平分 */
}

.large-module :deep(.el-card) {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.large-module :deep(.el-card__body) {
  flex: 1;
  overflow-y: auto;
}

.large-module::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #3b82f6, #8b5cf6);
  opacity: 0.7;
  transition: opacity 0.3s ease;
}

.large-module:hover {
  transform: translateY(-3px);
  box-shadow: 
    0 12px 32px rgba(0, 0, 0, 0.08),
    0 4px 12px rgba(59, 130, 246, 0.1);
  border-color: rgba(59, 130, 246, 0.3);
  background: white;
}

.large-module:hover::before {
  opacity: 1;
  height: 4px;
}

/* 第二行：4个小模块各占1/4宽度 */
.bottom-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.small-module {
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(226, 232, 240, 0.8);
  overflow: hidden;
  transition: all 0.3s ease;
  position: relative;
  box-shadow: 
    0 4px 12px rgba(0, 0, 0, 0.04),
    0 1px 2px rgba(0, 0, 0, 0.02);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  min-height: 200px; /* 整体卡片高度不变 */
  display: block !important; /* 强制block布局，避免flex平分 */
}

.small-module :deep(.el-card) {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.small-module :deep(.el-card__body) {
  flex: 1;
  overflow-y: auto;
}

.small-module::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, #3b82f6, #8b5cf6);
  opacity: 0.6;
  transition: opacity 0.3s ease;
}

.small-module:hover {
  transform: translateY(-2px);
  box-shadow: 
    0 8px 24px rgba(0, 0, 0, 0.08),
    0 2px 6px rgba(59, 130, 246, 0.1);
  border-color: rgba(59, 130, 246, 0.3);
  background: white;
}

.small-module:hover::before {
  opacity: 1;
  height: 3px;
}

/* 卡片内容区域自适应 - 优化间距 */
.large-module > :not(.card-header),
.small-module > :not(.card-header) {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

/* 优化列表项间距 */
.project-item,
.community-item,
.activity-item,
.notification-item,
.tech-item {
  padding: 12px 0;
}

.project-item:not(:last-child),
.community-item:not(:last-child),
.activity-item:not(:last-child),
.notification-item:not(:last-child),
.tech-item:not(:last-child) {
  border-bottom: 1px solid rgba(226, 232, 240, 0.6);
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .top-row {
    grid-template-columns: 1fr;
    min-height: auto;
  }
  
  .bottom-row {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .top-row {
    gap: 16px;
  }
  
  .bottom-row {
    grid-template-columns: 1fr;
    gap: 16px;
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 1200px) {
  .main-content {
    grid-template-columns: 1fr;
  }
}

/* 移除自定义card-header，使用Element Plus原生header */

/* 美化卡片header - 添加样式和图标效果 */
:deep(.el-card__header) {
  padding: 8px 16px !important;
  border-bottom: 1px solid rgba(226, 232, 240, 0.8) !important;
  background: linear-gradient(90deg, rgba(59, 130, 246, 0.08), rgba(139, 92, 246, 0.05), transparent) !important;
  position: relative;
  overflow: hidden;
}

/* header装饰线条 */
:deep(.el-card__header)::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, #3b82f6, #8b5cf6, #3b82f6);
  opacity: 0.7;
}

/* header悬停效果 */
:deep(.el-card):hover .el-card__header::before {
  opacity: 1;
  height: 3px;
}

:deep(.el-card__header h3) {
  margin: 0 !important;
  font-size: 14px !important;
  font-weight: 700 !important;
  color: #1a1a1a !important;
  display: flex !important;
  align-items: center !important;
  gap: 8px !important;
}

/* 图标样式 */
:deep(.el-card__header h3 .el-icon) {
  font-size: 16px;
  width: 16px;
  height: 16px;
}

/* 不同模块的图标颜色 */
.large-module:nth-child(1) :deep(.el-card__header h3 .el-icon) {
  color: #3b82f6;
}

.large-module:nth-child(2) :deep(.el-card__header h3 .el-icon) {
  color: #8b5cf6;
}

.small-module:nth-child(1) :deep(.el-card__header h3 .el-icon) {
  color: #10b981;
}

.small-module:nth-child(2) :deep(.el-card__header h3 .el-icon) {
  color: #f59e0b;
}

.small-module:nth-child(3) :deep(.el-card__header h3 .el-icon) {
  color: #ef4444;
}

.small-module:nth-child(4) :deep(.el-card__header h3 .el-icon) {
  color: #8b5cf6;
}

/* 移除伪元素图标样式，因为现在使用真实图标 */

/* header按钮样式 */
:deep(.el-card__header .el-button) {
  font-size: 12px !important;
  padding: 2px 8px !important;
  height: 24px !important;
  border-radius: 4px !important;
  font-weight: 500 !important;
}

:deep(.el-card__header .el-button--primary) {
  background: rgba(59, 130, 246, 0.1) !important;
  border-color: rgba(59, 130, 246, 0.3) !important;
  color: #3b82f6 !important;
}

:deep(.el-card__header .el-button--primary:hover) {
  background: rgba(59, 130, 246, 0.2) !important;
  border-color: #3b82f6 !important;
}

:deep(.el-card__header .el-button--text) {
  color: #64748b !important;
}

:deep(.el-card__header .el-button--text:hover) {
  color: #3b82f6 !important;
}

/* 卡片内容区域样式已经在各自模块中定义 */

/* 明亮科技风项目列表 */
.project-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 0;
}

.project-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: #f8fafc;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.project-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: linear-gradient(180deg, #3b82f6, #8b5cf6);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.project-item:hover {
  background: white;
  border-color: rgba(59, 130, 246, 0.3);
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
}

.project-item:hover::before {
  opacity: 1;
}

.project-info {
  flex: 1;
}

.project-name {
  font-size: 16px;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.project-name::before {
  content: '▸';
  color: #3b82f6;
  font-size: 12px;
}

.project-description {
  font-size: 14px;
  color: #64748b;
  margin-bottom: 12px;
  line-height: 1.5;
}

.project-meta {
  display: flex;
  gap: 20px;
  font-size: 12px;
  color: #94a3b8;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.project-progress {
  width: 240px;
}

.progress-label {
  font-size: 12px;
  color: #64748b;
  text-align: right;
  margin-top: 6px;
  font-weight: 500;
}

/* 明亮科技风活动列表 */
.activity-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 0;
}

.activity-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px;
  border-radius: 10px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
}

.activity-item:hover {
  background: white;
  border-color: rgba(59, 130, 246, 0.3);
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
}

.activity-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(139, 92, 246, 0.1));
  border: 1px solid rgba(59, 130, 246, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.activity-icon :deep(.el-icon) {
  font-size: 18px;
  width: 18px;
  height: 18px;
}

.activity-content {
  flex: 1;
}

.activity-title {
  font-size: 14px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 4px;
}

.activity-description {
  font-size: 13px;
  color: #64748b;
  margin-bottom: 6px;
  line-height: 1.4;
}

.activity-time {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 500;
}

/* 自然有人味 - 快速操作 */
.quick-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 0;
}

.action-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(226, 232, 240, 0.8);
  transition: all 0.3s ease;
  cursor: pointer;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

/* 图标 - 自然贴边设计 */
.action-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.3s ease;
}

.action-icon .el-icon {
  font-size: 20px;
  transition: all 0.3s ease;
}

/* 不同类型的基础颜色 */
.action-primary .action-icon {
  background: rgba(59, 130, 246, 0.1);
  border: 1px solid rgba(59, 130, 246, 0.2);
}

.action-primary .action-icon .el-icon {
  color: #3b82f6;
}

.action-success .action-icon {
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.action-success .action-icon .el-icon {
  color: #10b981;
}

.action-info .action-icon {
  background: rgba(6, 182, 212, 0.1);
  border: 1px solid rgba(6, 182, 212, 0.2);
}

.action-info .action-icon .el-icon {
  color: #06b6d4;
}

.action-warning .action-icon {
  background: rgba(245, 158, 11, 0.1);
  border: 1px solid rgba(245, 158, 11, 0.2);
}

.action-warning .action-icon .el-icon {
  color: #f59e0b;
}

/* 内容区域 */
.action-content {
  flex: 1;
  min-width: 0;
}

.action-label {
  font-size: 15px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 4px;
  transition: color 0.3s ease;
}

.action-desc {
  font-size: 12px;
  color: #64748b;
  line-height: 1.4;
  transition: color 0.3s ease;
}

/* 悬停效果 - 自然有人味 */
.action-item:hover {
  background: white;
  border-color: #e2e8f0;
  transform: translateY(-2px);
  box-shadow: 
    0 8px 24px rgba(0, 0, 0, 0.08),
    0 2px 6px rgba(0, 0, 0, 0.03);
}

.action-item:hover .action-icon {
  transform: scale(1.05);
}

.action-item:hover .action-icon .el-icon {
  transform: scale(1.1);
}

/* 不同类型悬停时的颜色增强 */
.action-primary:hover .action-icon {
  background: rgba(59, 130, 246, 0.15);
  border-color: #3b82f6;
}

.action-primary:hover .action-label {
  color: #3b82f6;
}

.action-success:hover .action-icon {
  background: rgba(16, 185, 129, 0.15);
  border-color: #10b981;
}

.action-success:hover .action-label {
  color: #10b981;
}

.action-info:hover .action-icon {
  background: rgba(6, 182, 212, 0.15);
  border-color: #06b6d4;
}

.action-info:hover .action-label {
  color: #06b6d4;
}

.action-warning:hover .action-icon {
  background: rgba(245, 158, 11, 0.15);
  border-color: #f59e0b;
}

.action-warning:hover .action-label {
  color: #f59e0b;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .action-item {
    padding: 14px;
    gap: 12px;
  }
  
  .action-icon {
    width: 36px;
    height: 36px;
  }
  
  .action-icon .el-icon {
    font-size: 18px;
  }
  
  .action-label {
    font-size: 14px;
  }
  
  .action-desc {
    font-size: 11px;
  }
}

/* 标准风格 - 系统通知 */
.notification-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 0;
}

.notification-item {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 16px;
  border-radius: 12px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-left: 4px solid transparent;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.notification-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.1), transparent);
}

.notification-item.unread {
  border-left-color: #3b82f6;
  background: white;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.1);
  animation: subtlePulse 3s infinite;
}

@keyframes subtlePulse {
  0%, 100% {
    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.1);
  }
  50% {
    box-shadow: 0 2px 12px rgba(59, 130, 246, 0.15);
  }
}

.notification-item:hover {
  transform: translateX(2px);
  border-color: #3b82f6;
  background: white;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
}

.notification-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(139, 92, 246, 0.1));
  border: 1px solid rgba(59, 130, 246, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.notification-icon :deep(.el-icon) {
  font-size: 18px;
  width: 18px;
  height: 18px;
}

.notification-content {
  flex: 1;
}

.notification-title {
  font-size: 14px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 4px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.notification-title::before {
  content: '';
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #3b82f6;
  display: inline-block;
}

.notification-item.unread .notification-title::before {
  background: #ef4444;
  animation: blink 1.5s infinite;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.notification-message {
  font-size: 13px;
  color: #64748b;
  margin-bottom: 6px;
  line-height: 1.5;
}

.notification-time {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 4px;
}

.notification-time::before {
  content: '🕒';
  font-size: 10px;
}

.notification-actions {
  flex-shrink: 0;
  display: flex;
  gap: 8px;
}

/* 标准风格 - 社区交流 */
.community-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 0;
}

.community-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  border-radius: 12px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
}

.community-item:hover {
  background: white;
  border-color: #3b82f6;
  transform: translateX(2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
}

.community-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(139, 92, 246, 0.1));
  border: 1px solid rgba(59, 130, 246, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.community-icon :deep(.el-icon) {
  font-size: 18px;
  width: 18px;
  height: 18px;
}

.community-content {
  flex: 1;
  min-width: 0; /* 防止文本溢出 */
}

.community-title {
  font-size: 14px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 6px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.community-meta {
  display: flex;
  gap: 16px;
  font-size: 12px;
  color: #64748b;
  margin-bottom: 6px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.community-description {
  font-size: 12px;
  color: #94a3b8;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.join-button {
  flex-shrink: 0;
  height: 32px;
  font-size: 12px;
  font-weight: 600;
  border-radius: 8px;
  padding: 0 16px;
}

/* 标准风格 - 技术栈展示 */
.tech-stack {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 0;
}

.tech-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  border-radius: 12px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
}

.tech-item:hover {
  background: white;
  border-color: #3b82f6;
  transform: translateX(2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
}

.tech-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  overflow: hidden;
  flex-shrink: 0;
  background: white;
  padding: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #e2e8f0;
}

.tech-icon img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.tech-info {
  flex: 1;
}

.tech-name {
  font-size: 14px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 2px;
}

.tech-version {
  font-size: 12px;
  color: #64748b;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 4px;
}

.tech-version::before {
  content: 'v';
  color: #94a3b8;
  font-size: 10px;
}

/* 响应式设计优化 */
@media (max-width: 768px) {
  .dashboard {
    padding: 16px;
  }
  
  .dashboard-title {
    font-size: 32px;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .main-content {
    gap: 24px;
  }
  
  .project-item {
    flex-direction: column;
    gap: 16px;
  }
  
  .project-progress {
    width: 100%;
  }
  
  .quick-actions {
    grid-template-columns: 1fr;
  }
}

/* 滚动条美化 */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #3b82f6, #8b5cf6);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, #60a5fa, #a78bfa);
}

/* 紧凑卡片样式 */
.compact-card {
  margin-bottom: 16px !important;
}

.compact-card .card-header {
  padding: 16px 20px 12px !important;
}

.compact-card .card-header h3 {
  font-size: 16px !important;
}

/* 紧凑通知列表 */
.compact-list .notification-item {
  padding: 12px 16px !important;
  gap: 12px !important;
}

.compact-list .notification-icon {
  width: 32px !important;
  height: 32px !important;
}

.compact-list .notification-title {
  font-size: 13px !important;
  margin-bottom: 2px !important;
}

.compact-list .notification-message {
  display: none !important;
}

.compact-list .notification-time {
  font-size: 11px !important;
}

/* 紧凑技术栈 */
.compact-stack .tech-item {
  padding: 12px 16px !important;
  gap: 12px !important;
}

.compact-stack .tech-icon {
  width: 32px !important;
  height: 32px !important;
}

.compact-stack .tech-name {
  font-size: 13px !important;
}

.compact-stack .tech-version {
  font-size: 11px !important;
}

.compact-stack .el-tag {
  display: none !important;
}

/* 优化快速操作卡片高度 */
.quick-actions {
  height: 100%;
  overflow-y: auto;
}

.quick-actions::-webkit-scrollbar {
  width: 4px;
}

.quick-actions::-webkit-scrollbar-thumb {
  background: rgba(59, 130, 246, 0.3);
  border-radius: 2px;
}

/* 平衡左右栏高度 */
.left-column, .right-column {
  display: flex;
  flex-direction: column;
}

.left-column .section-card,
.right-column .section-card {
  flex: 1;
  min-height: 0; /* 允许收缩 */
}

.left-column .section-card:last-child,
.right-column .section-card:last-child {
  margin-bottom: 0;
}
</style>

