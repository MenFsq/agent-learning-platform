<template>
  <header class="app-header">
    <!-- 左侧：Logo和导航 -->
    <div class="header-left">
      <div class="logo">
        <div class="logo-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2L2 7L12 12L22 7L12 2Z" fill="url(#gradient)" />
            <path d="M2 17L12 22L22 17" stroke="url(#gradient)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            <path d="M2 12L12 17L22 12" stroke="url(#gradient)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            <defs>
              <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#3b82f6" />
                <stop offset="100%" stop-color="#8b5cf6" />
              </linearGradient>
            </defs>
          </svg>
        </div>
        <h1 class="logo-text">Agent Learning</h1>
      </div>
      
      <!-- 主导航 -->
      <nav class="main-nav">
        <router-link 
          v-for="item in navItems" 
          :key="item.path"
          :to="item.path"
          class="nav-item"
          :class="{ active: $route.path === item.path }"
        >
          <component :is="item.icon" class="nav-icon" />
          <span class="nav-text">{{ item.name }}</span>
        </router-link>
      </nav>
    </div>

    <!-- 右侧：用户操作 -->
    <div class="header-right">
      <!-- 搜索框 -->
      <div class="search-box">
        <el-input
          v-model="searchQuery"
          placeholder="搜索项目、教程..."
          size="small"
          :prefix-icon="Search"
          class="search-input"
        />
      </div>

      <!-- 通知 -->
      <el-dropdown trigger="click" class="notification-dropdown">
        <div class="notification-btn">
          <el-badge :value="3" :max="99" class="badge">
            <Bell class="icon" />
          </el-badge>
        </div>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item>
              <div class="notification-item">
                <div class="notification-icon success">
                  <CheckCircle class="icon-small" />
                </div>
                <div class="notification-content">
                  <div class="notification-title">项目构建成功</div>
                  <div class="notification-time">2分钟前</div>
                </div>
              </div>
            </el-dropdown-item>
            <el-dropdown-item>
              <div class="notification-item">
                <div class="notification-icon warning">
                  <AlertTriangle class="icon-small" />
                </div>
                <div class="notification-content">
                  <div class="notification-title">系统更新可用</div>
                  <div class="notification-time">1小时前</div>
                </div>
              </div>
            </el-dropdown-item>
            <el-dropdown-item>
              <div class="notification-item">
                <div class="notification-icon info">
                  <Info class="icon-small" />
                </div>
                <div class="notification-content">
                  <div class="notification-title">新教程发布</div>
                  <div class="notification-time">3小时前</div>
                </div>
              </div>
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>

      <!-- 用户信息 -->
      <el-dropdown trigger="click" class="user-dropdown">
        <div class="user-info">
          <el-avatar :size="36" :src="user.avatar" class="user-avatar" />
          <div class="user-details">
            <div class="user-name">{{ user.name }}</div>
            <div class="user-role">{{ user.role }}</div>
          </div>
          <ChevronDown class="dropdown-arrow" />
        </div>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item>
              <User class="dropdown-icon" />
              个人资料
            </el-dropdown-item>
            <el-dropdown-item>
              <Settings class="dropdown-icon" />
              系统设置
            </el-dropdown-item>
            <el-dropdown-item divided>
              <LogOut class="dropdown-icon" />
              退出登录
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
// import { useRouter } from 'vue-router' // 暂时注释掉未使用的导入
import { 
  Home, 
  FolderKanban, 
  BookOpen, 
  Users,
  Settings as SettingsIcon,
  Search,
  Bell,
  CheckCircle,
  AlertTriangle,
  Info,
  User,
  Settings,
  LogOut,
  ChevronDown
} from 'lucide-vue-next'

// const router = useRouter() // 暂时注释掉未使用的变量
const searchQuery = ref('')

// 用户信息
const user = reactive({
  name: '小老虎 🐯',
  role: '管理员',
  avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=tiger&backgroundColor=3b82f6&hairColor=8b5cf6'
})

// 导航项
const navItems = [
  { path: '/', name: '仪表板', icon: Home },
  { path: '/projects', name: '项目', icon: FolderKanban },
  { path: '/learning', name: '学习', icon: BookOpen },
  { path: '/community', name: '社区', icon: Users },
  { path: '/settings', name: '设置', icon: SettingsIcon }
]
</script>

<style scoped>
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 32px;
  height: 72px;
  background: white;
  border-bottom: 1px solid #f0f2f5;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
  position: sticky;
  top: 0;
  z-index: 1000;
}

/* 左侧区域 */
.header-left {
  display: flex;
  align-items: center;
  gap: 48px;
}

/* Logo */
.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-text {
  font-size: 20px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0;
  background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* 主导航 */
.main-nav {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  border-radius: 10px;
  text-decoration: none;
  color: #666;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.nav-item:hover {
  background: #f5f7fa;
  color: #3b82f6;
}

.nav-item.active {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(139, 92, 246, 0.1));
  color: #3b82f6;
  font-weight: 600;
}

.nav-icon {
  width: 18px;
  height: 18px;
}

/* 右侧区域 */
.header-right {
  display: flex;
  align-items: center;
  gap: 24px;
}

/* 搜索框 */
.search-box {
  width: 280px;
}

.search-input :deep(.el-input__wrapper) {
  border-radius: 10px;
  border: 1px solid #e4e7ed;
  background: #f8fafc;
}

.search-input :deep(.el-input__wrapper:hover) {
  border-color: #cbd5e1;
}

.search-input :deep(.el-input__wrapper.is-focus) {
  border-color: #3b82f6;
  box-shadow: 0 0 0 1px rgba(59, 130, 246, 0.2);
}

/* 通知 */
.notification-btn {
  padding: 8px;
  border-radius: 10px;
  cursor: pointer;
  transition: background 0.2s ease;
}

.notification-btn:hover {
  background: #f5f7fa;
}

.notification-btn .icon {
  width: 20px;
  height: 20px;
  color: #64748b;
}

.notification-btn:hover .icon {
  color: #3b82f6;
}

.badge :deep(.el-badge__content) {
  border: 2px solid white;
}

/* 通知下拉菜单 */
.notification-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  min-width: 280px;
}

.notification-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.notification-icon.success {
  background: rgba(34, 197, 94, 0.1);
  color: #16a34a;
}

.notification-icon.warning {
  background: rgba(245, 158, 11, 0.1);
  color: #d97706;
}

.notification-icon.info {
  background: rgba(59, 130, 246, 0.1);
  color: #2563eb;
}

.icon-small {
  width: 16px;
  height: 16px;
}

.notification-content {
  flex: 1;
}

.notification-title {
  font-size: 14px;
  font-weight: 500;
  color: #1a1a1a;
  margin-bottom: 2px;
}

.notification-time {
  font-size: 12px;
  color: #94a3b8;
}

/* 用户信息 */
.user-dropdown {
  cursor: pointer;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px;
  border-radius: 12px;
  transition: background 0.2s ease;
}

.user-info:hover {
  background: #f5f7fa;
}

.user-avatar {
  border: 2px solid #f0f2f5;
}

.user-details {
  text-align: left;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  color: #1a1a1a;
}

.user-role {
  font-size: 12px;
  color: #94a3b8;
}

.dropdown-arrow {
  width: 16px;
  height: 16px;
  color: #94a3b8;
}

/* 下拉菜单图标 */
.dropdown-icon {
  width: 16px;
  height: 16px;
  margin-right: 8px;
  vertical-align: middle;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .app-header {
    padding: 0 20px;
  }
  
  .header-left {
    gap: 24px;
  }
  
  .search-box {
    width: 200px;
  }
  
  .nav-text {
    display: none;
  }
  
  .nav-item {
    padding: 12px;
  }
}

@media (max-width: 768px) {
  .search-box {
    display: none;
  }
  
  .logo-text {
    display: none;
  }
}
</style>