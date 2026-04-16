<template>
  <div class="settings-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">
            <Settings2 class="title-icon" />
            系统设置
          </h1>
          <p class="page-subtitle">
            配置你的Agent Learning Platform，个性化你的工作环境
          </p>
        </div>
      </div>
    </div>

    <!-- 设置内容 -->
    <div class="settings-content">
      <!-- 左侧：设置导航 -->
      <div class="settings-sidebar">
        <div class="sidebar-section">
          <h4 class="section-title">设置分类</h4>
          <div class="nav-list">
            <div
              v-for="item in navItems"
              :key="item.id"
              class="nav-item"
              :class="{ active: activeTab === item.id }"
              @click="activeTab = item.id"
            >
              <component :is="item.icon" class="nav-icon" />
              <span class="nav-text">{{ item.name }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧：设置详情 -->
      <div class="settings-detail">
        <!-- 账户设置 -->
        <div v-if="activeTab === 'account'" class="settings-section">
          <h3 class="section-title">账户设置</h3>
          <div class="settings-form">
            <el-form :model="accountForm" label-width="120px">
              <el-form-item label="用户名">
                <el-input v-model="accountForm.username" placeholder="请输入用户名" />
              </el-form-item>
              <el-form-item label="邮箱">
                <el-input v-model="accountForm.email" placeholder="请输入邮箱" />
              </el-form-item>
              <el-form-item label="头像">
                <div class="avatar-upload">
                  <el-avatar :size="80" :src="accountForm.avatar" />
                  <el-upload
                    action="#"
                    :show-file-list="false"
                    :before-upload="handleAvatarUpload"
                  >
                    <el-button type="primary" :icon="Upload">更换头像</el-button>
                  </el-upload>
                </div>
              </el-form-item>
              <el-form-item label="个人简介">
                <el-input
                  v-model="accountForm.bio"
                  type="textarea"
                  :rows="3"
                  placeholder="介绍一下你自己..."
                />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="saveAccountSettings">保存设置</el-button>
                <el-button @click="resetAccountForm">重置</el-button>
              </el-form-item>
            </el-form>
          </div>
        </div>

        <!-- 安全设置 -->
        <div v-else-if="activeTab === 'security'" class="settings-section">
          <h3 class="section-title">安全设置</h3>
          <div class="settings-form">
            <el-form label-width="120px">
              <el-form-item label="当前密码">
                <el-input v-model="securityForm.currentPassword" type="password" placeholder="请输入当前密码" />
              </el-form-item>
              <el-form-item label="新密码">
                <el-input v-model="securityForm.newPassword" type="password" placeholder="请输入新密码" />
              </el-form-item>
              <el-form-item label="确认新密码">
                <el-input v-model="securityForm.confirmPassword" type="password" placeholder="请再次输入新密码" />
              </el-form-item>
              <el-form-item label="两步验证">
                <el-switch v-model="securityForm.twoFactorEnabled" />
                <span class="switch-label">启用两步验证增强账户安全</span>
              </el-form-item>
              <el-form-item label="登录通知">
                <el-switch v-model="securityForm.loginNotifications" />
                <span class="switch-label">新设备登录时发送通知</span>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="updatePassword">更新密码</el-button>
                <el-button @click="resetSecurityForm">重置</el-button>
              </el-form-item>
            </el-form>
          </div>
        </div>

        <!-- 通知设置 -->
        <div v-else-if="activeTab === 'notifications'" class="settings-section">
          <h3 class="section-title">通知设置</h3>
          <div class="settings-form">
            <el-form label-width="120px">
              <el-form-item label="邮件通知">
                <el-switch v-model="notificationForm.emailNotifications" />
                <span class="switch-label">接收邮件通知</span>
              </el-form-item>
              <el-form-item label="社区动态">
                <el-switch v-model="notificationForm.communityUpdates" />
                <span class="switch-label">关注用户的动态更新</span>
              </el-form-item>
              <el-form-item label="项目更新">
                <el-switch v-model="notificationForm.projectUpdates" />
                <span class="switch-label">项目进度和任务更新</span>
              </el-form-item>
              <el-form-item label="系统公告">
                <el-switch v-model="notificationForm.systemAnnouncements" />
                <span class="switch-label">平台更新和维护通知</span>
              </el-form-item>
              <el-form-item label="营销信息">
                <el-switch v-model="notificationForm.marketingEmails" />
                <span class="switch-label">产品更新和优惠信息</span>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="saveNotificationSettings">保存设置</el-button>
                <el-button @click="resetNotificationForm">重置</el-button>
              </el-form-item>
            </el-form>
          </div>
        </div>

        <!-- 外观设置 -->
        <div v-else-if="activeTab === 'appearance'" class="settings-section">
          <h3 class="section-title">外观设置</h3>
          <div class="settings-form">
            <el-form label-width="120px">
              <el-form-item label="主题模式">
                <el-radio-group v-model="appearanceForm.theme">
                  <el-radio label="light">浅色模式</el-radio>
                  <el-radio label="dark">深色模式</el-radio>
                  <el-radio label="auto">跟随系统</el-radio>
                </el-radio-group>
              </el-form-item>
              <el-form-item label="语言">
                <el-select v-model="appearanceForm.language" placeholder="选择语言">
                  <el-option label="简体中文" value="zh-CN" />
                  <el-option label="English" value="en" />
                </el-select>
              </el-form-item>
              <el-form-item label="字体大小">
                <el-slider
                  v-model="appearanceForm.fontSize"
                  :min="12"
                  :max="18"
                  :step="1"
                  show-input
                />
              </el-form-item>
              <el-form-item label="动画效果">
                <el-switch v-model="appearanceForm.animations" />
                <span class="switch-label">启用界面动画效果</span>
              </el-form-item>
              <el-form-item label="紧凑模式">
                <el-switch v-model="appearanceForm.compactMode" />
                <span class="switch-label">减少界面间距，显示更多内容</span>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="saveAppearanceSettings">保存设置</el-button>
                <el-button @click="resetAppearanceForm">重置</el-button>
              </el-form-item>
            </el-form>
          </div>
        </div>

        <!-- API设置 -->
        <div v-else-if="activeTab === 'api'" class="settings-section">
          <h3 class="section-title">API设置</h3>
          <div class="settings-form">
            <el-form label-width="120px">
              <el-form-item label="OpenAI API Key">
                <el-input
                  v-model="apiForm.openaiKey"
                  type="password"
                  placeholder="输入OpenAI API密钥"
                  show-password
                />
                <div class="form-help">
                  <el-link type="primary" href="https://platform.openai.com/api-keys" target="_blank">
                    获取OpenAI API密钥
                  </el-link>
                </div>
              </el-form-item>
              <el-form-item label="模型选择">
                <el-select v-model="apiForm.defaultModel" placeholder="选择默认模型">
                  <el-option label="GPT-4" value="gpt-4" />
                  <el-option label="GPT-3.5 Turbo" value="gpt-3.5-turbo" />
                  <el-option label="Claude 3" value="claude-3" />
                </el-select>
              </el-form-item>
              <el-form-item label="请求超时">
                <el-input-number
                  v-model="apiForm.timeout"
                  :min="10"
                  :max="120"
                  :step="5"
                />
                <span class="unit-label">秒</span>
              </el-form-item>
              <el-form-item label="最大令牌数">
                <el-input-number
                  v-model="apiForm.maxTokens"
                  :min="100"
                  :max="4000"
                  :step="100"
                />
              </el-form-item>
              <el-form-item label="温度设置">
                <el-slider
                  v-model="apiForm.temperature"
                  :min="0"
                  :max="1"
                  :step="0.1"
                  show-input
                />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="testApiConnection">测试连接</el-button>
                <el-button @click="saveApiSettings">保存设置</el-button>
              </el-form-item>
            </el-form>
          </div>
        </div>

        <!-- 数据设置 -->
        <div v-else-if="activeTab === 'data'" class="settings-section">
          <h3 class="section-title">数据设置</h3>
          <div class="settings-form">
            <el-form label-width="120px">
              <el-form-item label="数据备份">
                <el-button :icon="Download" @click="backupData">备份数据</el-button>
                <div class="form-help">
                  备份所有项目、Agent和设置数据
                </div>
              </el-form-item>
              <el-form-item label="数据恢复">
                <el-upload
                  action="#"
                  :show-file-list="false"
                  :before-upload="handleDataRestore"
                >
                  <el-button :icon="Upload">恢复数据</el-button>
                </el-upload>
                <div class="form-help">
                  从备份文件恢复数据（将覆盖现有数据）
                </div>
              </el-form-item>
              <el-form-item label="导出数据">
                <el-button :icon="FileText" @click="exportData">导出为JSON</el-button>
                <el-button :icon="FileSpreadsheet" @click="exportCSV">导出为CSV</el-button>
              </el-form-item>
              <el-form-item label="清除缓存">
                <el-button :icon="Trash2" @click="clearCache">清除缓存</el-button>
                <div class="form-help">
                  清除本地缓存数据，不影响云端数据
                </div>
              </el-form-item>
              <el-form-item label="删除账户">
                <el-button type="danger" :icon="AlertTriangle" @click="deleteAccount">
                  删除账户
                </el-button>
                <div class="form-help danger">
                  此操作不可恢复，将删除所有数据
                </div>
              </el-form-item>
            </el-form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Settings2,
  User,
  Shield,
  Bell,
  Palette,
  Cpu,
  Database,
  Upload,
  Download,
  FileText,
  FileSpreadsheet,
  Trash2,
  AlertTriangle
} from 'lucide-vue-next'

// 导航项
const navItems = [
  { id: 'account', name: '账户设置', icon: User },
  { id: 'security', name: '安全设置', icon: Shield },
  { id: 'notifications', name: '通知设置', icon: Bell },
  { id: 'appearance', name: '外观设置', icon: Palette },
  { id: 'api', name: 'API设置', icon: Cpu },
  { id: 'data', name: '数据设置', icon: Database }
]

// 当前激活的标签页
const activeTab = ref('account')

// 账户表单
const accountForm = ref({
  username: '小老虎',
  email: 'tiger@agent-learning.com',
  avatar: 'https://api.dicebear.com/7.x/bottts/svg?seed=agent-learning',
  bio: 'AI Agent开发者，专注于LangChain和Vue 3技术栈'
})

// 安全表单
const securityForm = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: '',
  twoFactorEnabled: false,
  loginNotifications: true
})

// 通知表单
const notificationForm = ref({
  emailNotifications: true,
  communityUpdates: true,
  projectUpdates: true,
  systemAnnouncements: true,
  marketingEmails: false
})

// 外观表单
const appearanceForm = ref({
  theme: 'dark',
  language: 'zh-CN',
  fontSize: 14,
  animations: true,
  compactMode: false
})

// API表单
const apiForm = ref({
  openaiKey: '',
  defaultModel: 'gpt-3.5-turbo',
  timeout: 30,
  maxTokens: 2000,
  temperature: 0.7
})

// 方法
const saveAccountSettings = () => {
  ElMessage.success('账户设置已保存')
}

const resetAccountForm = () => {
  accountForm.value = {
    username: '小老虎',
    email: 'tiger@agent-learning.com',
    avatar: 'https://api.dicebear.com/7.x/bottts/svg?seed=agent-learning',
    bio: 'AI Agent开发者，专注于LangChain和Vue 3技术栈'
  }
  ElMessage.info('账户设置已重置')
}

const updatePassword = () => {
  if (securityForm.value.newPassword !== securityForm.value.confirmPassword) {
    ElMessage.error('两次输入的密码不一致')
    return
  }
  ElMessage.success('密码更新成功')
  securityForm.value.currentPassword = ''
  securityForm.value.newPassword = ''
  securityForm.value.confirmPassword = ''
}

const resetSecurityForm = () => {
  securityForm.value = {
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
    twoFactorEnabled: false,
    loginNotifications: true
  }
  ElMessage.info('安全设置已重置')
}

const saveNotificationSettings = () => {
  ElMessage.success('通知设置已保存')
}

const resetNotificationForm = () => {
  notificationForm.value = {
    emailNotifications: true,
    communityUpdates: true,
    projectUpdates: true,
    systemAnnouncements: true,
    marketingEmails: false
  }
  ElMessage.info('通知设置已重置')
}

const saveAppearanceSettings = () => {
  ElMessage.success('外观设置已保存')
}

const resetAppearanceForm = () => {
  appearanceForm.value = {
    theme: 'dark',
    language: 'zh-CN',
    fontSize: 14,
    animations: true,
    compactMode: false
  }
  ElMessage.info('外观设置已重置')
}

const testApiConnection = () => {
  ElMessage.info('正在测试API连接...')
  setTimeout(() => {
    ElMessage.success('API连接测试成功')
  }, 1000)
}

const saveApiSettings = () => {
  ElMessage.success('API设置已保存')
}

const backupData = () => {
  ElMessage.success('数据备份已开始，请稍候...')
}

const handleDataRestore = (_file: any) => {
  ElMessageBox.confirm(
    '恢复数据将覆盖现有数据，确定要继续吗？',
    '确认恢复',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    ElMessage.success('数据恢复已开始')
  })
  return false
}

const exportData = () => {
  ElMessage.success('数据导出为JSON已开始')
}

const exportCSV = () => {
  ElMessage.success('数据导出为CSV已开始')
}

const clearCache = () => {
  ElMessageBox.confirm(
    '确定要清除缓存吗？',
    '确认清除',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    ElMessage.success('缓存已清除')
  })
}

const deleteAccount = () => {
  ElMessageBox.confirm(
    '确定要删除账户吗？此操作不可恢复！',
    '确认删除',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'error'
    }
  ).then(() => {
    ElMessage.success('账户删除请求已提交')
  })
}

const handleAvatarUpload = (file: any) => {
  // 模拟上传
  const reader = new FileReader()
  reader.onload = (e) => {
    accountForm.value.avatar = e.target?.result as string
    ElMessage.success('头像上传成功')
  }
  reader.readAsDataURL(file)
  return false
}
</script>

<style scoped>
.settings-page {
  min-height: 100vh;
  background: var(--app-bg);
}

.page-header {
  padding: 24px 32px;
  border-bottom: 1px solid var(--line-soft);
  background: var(--app-bg-elevated);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 24px;
}

.title-section {
  flex: 1;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 24px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 8px 0;
}

.title-icon {
  width: 28px;
  height: 28px;
  color: var(--color-primary);
}

.page-subtitle {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
  line-height: 1.5;
}

.settings-content {
  display: flex;
  min-height: calc(100vh - 120px);
}

.settings-sidebar {
  width: 240px;
  border-right: 1px solid var(--line-soft);
  background: var(--app-bg-elevated);
  padding: 24px 0;
}

.sidebar-section {
  padding: 0 20px;
}

.sidebar-section .section-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-secondary);
  margin: 0 0 16px 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.nav-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  color: var(--text-secondary);

  &:hover {
    background: var(--app-bg);
    color: var(--text-primary);
  }

  &.active {
    background: var(--color-primary);
    color: white;
  }
}

.nav-icon {
  width: 18px;
  height: 18px;
}

.nav-text {
  font-size: 14px;
  font-weight: 500;
}

.settings-detail {
  flex: 1;
  padding: 32px;
  overflow-y: auto;
}

.settings-section {
  max-width: 800px;
  margin-bottom: 40px;
}

.settings-section .section-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 24px 0;
}

.settings-form {
  background: var(--app-bg-elevated);
  border: 1px solid var(--line-soft);
  border-radius: 12px;
  padding: 24px;
}

.avatar-upload {
  display: flex;
  align-items: center;
  gap: 20px;
}

.switch-label {
  margin-left: 12px;
  font-size: 14px;
  color: var(--text-secondary);
}

.form-help {
  margin-top: 8px;
  font-size: 12px;
  color: var(--text-muted);

  &.danger {
    color: var(--color-error);
  }
}

.unit-label {
  margin-left: 8px;
  font-size: 14px;
  color: var(--text-secondary);
}

@media (max-width: 768px) {
  .settings-content {
    flex-direction: column;
  }

  .settings-sidebar {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid var(--line-soft);
  }

  .nav-list {
    flex-direction: row;
    overflow-x: auto;
    padding-bottom: 8px;
  }

  .nav-item {
    flex-shrink: 0;
  }

  .settings-detail {
    padding: 16px;
  }

  .page-header {
    padding: 16px;
  }
}
</style>
