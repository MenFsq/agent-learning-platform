<template>
  <header class="app-header" :class="{ 'is-scrolled': isScrolled }">
    <div class="header-shell page-container">
      <div class="header-left">
        <router-link to="/" class="brand">
          <span class="brand-mark">
            <BrainCircuit />
          </span>
          <span class="brand-copy">
            <strong>Agent Learning</strong>
            <small>AI Agent Workspace</small>
          </span>
        </router-link>

        <nav class="main-nav" aria-label="主导航">
          <router-link
            v-for="item in navItems"
            :key="item.path"
            :to="item.path"
            class="nav-item"
            :class="{ active: route.path === item.path }"
          >
            <component :is="item.icon" class="nav-icon" />
            <span class="nav-text">{{ item.name }}</span>
          </router-link>
        </nav>
      </div>

      <div class="header-right">
        <div class="search-box">
          <el-input
            v-model="searchQuery"
            placeholder="搜索项目、教程、Agent..."
            :prefix-icon="Search"
            class="search-input"
          />
        </div>

        <button
          type="button"
          class="icon-button"
          :aria-label="theme === 'dark' ? '切换到浅色模式' : '切换到深色模式'"
          @click="appStore.toggleTheme"
        >
          <SunMedium v-if="theme === 'dark'" class="icon" />
          <MoonStar v-else class="icon" />
        </button>

        <el-dropdown trigger="click" placement="bottom-end" popper-class="header-dropdown-popper">
          <button type="button" class="icon-button">
            <el-badge :value="unreadCount" :hidden="unreadCount === 0" :max="99">
              <Bell class="icon" />
            </el-badge>
          </button>
          <template #dropdown>
            <el-dropdown-menu class="menu-panel">
              <el-dropdown-item
                v-for="item in notificationPreview"
                :key="item.title"
                class="menu-item"
              >
                <div class="notice-item">
                  <span class="notice-dot" :class="item.tone"></span>
                  <div>
                    <div class="notice-title">{{ item.title }}</div>
                    <div class="notice-time">{{ item.time }}</div>
                  </div>
                </div>
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>

        <el-dropdown trigger="click" placement="bottom-end" popper-class="header-dropdown-popper">
          <button type="button" class="profile-button">
            <el-avatar :size="34" :src="user.avatar" />
            <div class="profile-copy">
              <span>{{ user.name }}</span>
              <small>{{ user.role }}</small>
            </div>
            <ChevronDown class="profile-arrow" />
          </button>
          <template #dropdown>
            <el-dropdown-menu class="menu-panel">
              <el-dropdown-item class="menu-item">
                <UserRound class="dropdown-icon" />
                个人资料
              </el-dropdown-item>
              <el-dropdown-item class="menu-item">
                <Sparkles class="dropdown-icon" />
                工作台偏好
              </el-dropdown-item>
              <el-dropdown-item class="menu-item">
                <Settings2 class="dropdown-icon" />
                系统设置
              </el-dropdown-item>
              <el-dropdown-item class="menu-item" divided @click="resetLocalProfile">
                <LogOut class="dropdown-icon" />
                清空本地资料
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  Bell,
  BookOpen,
  BrainCircuit,
  ChevronDown,
  FolderKanban,
  LayoutDashboard,
  MoonStar,
  Search,
  Settings2,
  Sparkles,
  SunMedium,
  UserRound,
  LogOut,
  Users,
  FileCode,
  Bot
} from 'lucide-vue-next'
import { storeToRefs } from 'pinia'

import { useAppStore } from '@/store/app'

const route = useRoute()
const router = useRouter()
const appStore = useAppStore()
const { theme } = storeToRefs(appStore)

const searchQuery = ref('')
const isScrolled = ref(false)

const defaultUser = {
  name: '小老虎',
  role: 'Workspace Owner',
  avatar: 'https://api.dicebear.com/7.x/bottts/svg?seed=agent-learning'
}

const user = reactive({ ...defaultUser })

const syncUserFromStorage = () => {
  const rawUser = localStorage.getItem('user')
  if (!rawUser) {
    Object.assign(user, defaultUser)
    return
  }

  try {
    const parsedUser = JSON.parse(rawUser) as {
      name?: string
      username?: string
      role?: string
      avatar?: string
    }
    user.name = parsedUser.name || parsedUser.username || user.name
    user.role = parsedUser.role || user.role
    user.avatar = parsedUser.avatar || user.avatar
  } catch (_error) {
    localStorage.removeItem('user')
    Object.assign(user, defaultUser)
  }
}

const resetLocalProfile = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user')
  syncUserFromStorage()
  // 跳转到登录页面
  router.push('/login')
}

const navItems = [
  { path: '/', name: '仪表板', icon: LayoutDashboard },
  { path: '/projects', name: '项目', icon: FolderKanban },
  { path: '/agent', name: 'Agent', icon: Bot },
  { path: '/learning', name: '学习', icon: BookOpen },
  { path: '/community', name: '社区', icon: Users },
  { path: '/api-docs', name: 'API文档', icon: FileCode },
  { path: '/settings', name: '设置', icon: Settings2 }
]

const notificationPreview = [
  { title: '项目构建成功，部署环境已同步', time: '2 分钟前', tone: 'success' },
  { title: '新的 LangChain 学习路径已上线', time: '18 分钟前', tone: 'info' },
  { title: '社区精选问答更新，适合继续阅读', time: '1 小时前', tone: 'accent' }
]

const unreadCount = computed(() => notificationPreview.length)

const handleScroll = () => {
  isScrolled.value = window.scrollY > 8
}

onMounted(() => {
  syncUserFromStorage()
  handleScroll()
  window.addEventListener('scroll', handleScroll, { passive: true })
  window.addEventListener('storage', syncUserFromStorage)
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll)
  window.removeEventListener('storage', syncUserFromStorage)
})
</script>

<style scoped lang="scss">
@use '@/styles/mixins' as *;

.app-header {
  position: fixed;
  inset: 0 0 auto;
  height: var(--header-height);
  z-index: 1000;
  border-bottom: 1px solid transparent;
  transition:
    background var(--transition-base),
    border-color var(--transition-base),
    box-shadow var(--transition-base);

  &::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(180deg, rgba(7, 10, 18, 0.74), rgba(7, 10, 18, 0.4));
    backdrop-filter: blur(calc(var(--blur-glass) + 6px));
    -webkit-backdrop-filter: blur(calc(var(--blur-glass) + 6px));
    border-bottom: 1px solid var(--line-soft);
  }
}

[data-theme='light'] .app-header::before {
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.84), rgba(255, 255, 255, 0.72));
}

.app-header.is-scrolled {
  border-color: var(--line-soft);
  box-shadow: var(--shadow-soft);
}

.header-shell {
  position: relative;
  z-index: 1;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}

.header-left,
.header-right {
  display: flex;
  align-items: center;
}

.header-left {
  gap: 28px;
  min-width: 0;
  flex: 1 1 auto;
}

.header-right {
  gap: 12px;
  flex-shrink: 0;
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.brand-mark {
  width: 42px;
  height: 42px;
  border-radius: 14px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.88), rgba(139, 92, 246, 0.82));
  border: 1px solid rgba(191, 219, 254, 0.34);
  color: #ffffff;
  box-shadow: 0 12px 28px rgba(59, 130, 246, 0.28);
}

[data-theme='light'] .brand-mark {
  background: linear-gradient(135deg, rgba(29, 78, 216, 0.94), rgba(124, 58, 237, 0.88));
  border-color: rgba(59, 130, 246, 0.22);
  color: #ffffff;
}

.brand-copy {
  display: flex;
  flex-direction: column;
  gap: 2px;
  line-height: 1.1;

  strong {
    font-size: 15px;
    font-weight: 600;
    letter-spacing: 0.02em;
    color: var(--text-primary);
  }

  small {
    font-size: 11px;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.12em;
  }
}

.main-nav {
  @include glass-panel(rgba(255, 255, 255, 0.03), var(--line-soft));
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px;
  border-radius: 999px;
  min-width: 0;
}

[data-theme='light'] .main-nav {
  background: rgba(255, 255, 255, 0.74);
}

.nav-item {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  border-radius: 999px;
  color: var(--text-secondary);
  flex: 0 0 auto;
  transition:
    color var(--transition-fast),
    background var(--transition-fast),
    transform var(--transition-fast);

  &:hover {
    color: var(--text-primary);
    background: rgba(255, 255, 255, 0.05);
    transform: translateY(-1px);
  }

  &.active {
    color: #ffffff;
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.92), rgba(6, 182, 212, 0.82));
    box-shadow: 0 12px 24px rgba(59, 130, 246, 0.22);
  }
}

[data-theme='light'] .nav-item.active {
  color: #ffffff;
}

.nav-icon {
  width: 16px;
  height: 16px;
}

.nav-text {
  font-size: 13px;
  font-weight: 500;
}

.search-box {
  width: min(28vw, 280px);
}

.search-input :deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, 0.03);
  box-shadow: none;
  border-radius: 14px;
  min-height: 42px;
  border: 1px solid var(--line-soft);
  transition:
    border-color var(--transition-fast),
    box-shadow var(--transition-fast),
    background var(--transition-fast);
}

.search-input :deep(.el-input__wrapper.is-focus) {
  border-color: rgba(59, 130, 246, 0.48);
  box-shadow: var(--glow-primary);
}

.search-input :deep(.el-input__inner) {
  color: var(--text-primary);
}

.icon-button,
.profile-button {
  @include glass-panel(rgba(255, 255, 255, 0.03), var(--line-soft));
  border-radius: 14px;
  border: 0;
  color: var(--text-secondary);
  min-height: 42px;
  transition:
    transform var(--transition-fast),
    border-color var(--transition-fast),
    color var(--transition-fast),
    background var(--transition-fast);
  cursor: pointer;

  &:hover {
    transform: translateY(-1px);
    color: var(--text-primary);
    border-color: var(--line-strong);
  }
}

.icon-button {
  width: 42px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.icon {
  width: 18px;
  height: 18px;
}

.profile-button {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 4px 10px 4px 6px;
}

.profile-copy {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  line-height: 1.1;

  span {
    font-size: 13px;
    font-weight: 600;
    color: var(--text-primary);
  }

  small {
    font-size: 11px;
    color: var(--text-muted);
  }
}

.profile-arrow,
.dropdown-icon {
  width: 16px;
  height: 16px;
}

.menu-panel {
  padding: 6px;
  background: transparent;
}

:deep(.menu-panel .el-dropdown-menu__item) {
  border-radius: 12px;
  color: var(--text-secondary);
  transition:
    color var(--transition-fast),
    background-color var(--transition-fast);
}

:deep(.menu-panel .el-dropdown-menu__item:hover),
:deep(.menu-panel .el-dropdown-menu__item:focus) {
  background: rgba(59, 130, 246, 0.14);
  color: var(--text-primary);
}

[data-theme='light'] :deep(.menu-panel .el-dropdown-menu__item:hover),
[data-theme='light'] :deep(.menu-panel .el-dropdown-menu__item:focus) {
  background: rgba(59, 130, 246, 0.1);
  color: var(--text-primary);
}

:deep(.header-dropdown-popper .el-dropdown-menu__item:hover),
:deep(.header-dropdown-popper .el-dropdown-menu__item:focus),
:deep(.header-dropdown-popper .el-dropdown-menu__item:not(.is-disabled):hover) {
  background-color: rgba(59, 130, 246, 0.14) !important;
  color: var(--text-primary) !important;
}

[data-theme='light'] :deep(.header-dropdown-popper .el-dropdown-menu__item:hover),
[data-theme='light'] :deep(.header-dropdown-popper .el-dropdown-menu__item:focus),
[data-theme='light'] :deep(.header-dropdown-popper .el-dropdown-menu__item:not(.is-disabled):hover) {
  background-color: rgba(59, 130, 246, 0.1) !important;
  color: var(--text-primary) !important;
}

.notice-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  min-width: 280px;
  padding: 6px 4px;
}

.notice-dot {
  width: 9px;
  height: 9px;
  border-radius: 999px;
  margin-top: 6px;
  flex-shrink: 0;

  &.success {
    background: var(--color-success);
  }

  &.info {
    background: var(--color-primary);
  }

  &.accent {
    background: var(--color-accent);
  }
}

.notice-title {
  font-size: 13px;
  color: var(--text-primary);
}

.notice-time {
  margin-top: 4px;
  font-size: 11px;
  color: var(--text-muted);
}

.icon-button :deep(.el-badge__content) {
  border-color: var(--app-bg-elevated);
}

@media (max-width: 1180px) {
  .nav-text,
  .profile-copy {
    display: none;
  }

  .main-nav {
    padding: 6px;
  }

  .nav-item {
    padding-inline: 12px;
  }
}

@media (max-width: 920px) {
  .search-box {
    display: none;
  }

  .header-shell {
    gap: 12px;
  }

  .header-left {
    gap: 14px;
  }
}

@media (max-width: 720px) {
  .header-shell {
    gap: 10px;
  }

  .header-left {
    gap: 10px;
  }

  .brand-copy small,
  .brand-copy strong {
    display: none;
  }

  .main-nav {
    gap: 2px;
    flex: 1 1 auto;
    overflow-x: auto;
    overflow-y: hidden;
    scrollbar-width: none;
    -ms-overflow-style: none;
    padding-inline: 4px;
  }

  .main-nav::-webkit-scrollbar {
    display: none;
  }

  .nav-item {
    padding: 10px;
  }

  .header-right {
    gap: 8px;
  }

  .profile-button {
    padding-inline: 6px;
  }

  .profile-arrow {
    display: none;
  }
}

@media (max-width: 560px) {
  .header-shell {
    gap: 8px;
  }

  .header-left {
    gap: 8px;
  }

  .brand-mark {
    width: 38px;
    height: 38px;
    border-radius: 12px;
  }

  .icon-button,
  .profile-button {
    min-height: 38px;
  }

  .icon-button {
    width: 38px;
  }

  .profile-button {
    padding: 2px;
  }
}
</style>

<style lang="scss">
.header-dropdown-popper {
  --el-dropdown-menuItem-hover-fill: rgba(59, 130, 246, 0.14);
  --el-dropdown-menuItem-hover-color: var(--text-primary);
}

[data-theme='light'] .header-dropdown-popper {
  --el-dropdown-menuItem-hover-fill: rgba(59, 130, 246, 0.1);
  --el-dropdown-menuItem-hover-color: var(--text-primary);
}

.header-dropdown-popper .el-dropdown-menu__item:not(.is-disabled):hover,
.header-dropdown-popper .el-dropdown-menu__item:focus,
.header-dropdown-popper .el-dropdown-menu__item.hover {
  background-color: var(--el-dropdown-menuItem-hover-fill) !important;
  color: var(--el-dropdown-menuItem-hover-color) !important;
}
</style>