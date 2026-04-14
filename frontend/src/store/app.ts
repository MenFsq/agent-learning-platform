import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface AppState {
  version: string
  theme: 'light' | 'dark'
  sidebarCollapsed: boolean
  loading: boolean
  notifications: Notification[]
}

export interface Notification {
  id: string
  type: 'success' | 'warning' | 'error' | 'info'
  title: string
  message: string
  timestamp: Date
  read: boolean
}

export const useAppStore = defineStore('app', () => {
  // 状态
  const version = ref('1.0.0')
  const theme = ref<'light' | 'dark'>('dark')
  const sidebarCollapsed = ref(false)
  const loading = ref(false)
  const notifications = ref<Notification[]>([])

  // 计算属性
  const unreadNotifications = computed(() => 
    notifications.value.filter(n => !n.read).length
  )

  const appTitle = computed(() => 'Agent Learning Platform')

  const applyTheme = (nextTheme: 'light' | 'dark') => {
    theme.value = nextTheme
    localStorage.setItem('theme', nextTheme)
    document.documentElement.setAttribute('data-theme', nextTheme)
  }

  // 动作
  const initialize = () => {
    const savedTheme = localStorage.getItem('theme')
    const nextTheme = savedTheme === 'light' || savedTheme === 'dark' ? savedTheme : 'dark'

    applyTheme(nextTheme)
  }

  const toggleTheme = () => {
    applyTheme(theme.value === 'light' ? 'dark' : 'light')
  }

  const toggleSidebar = () => {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }

  const setLoading = (isLoading: boolean) => {
    loading.value = isLoading
  }

  const addNotification = (notification: Omit<Notification, 'id' | 'timestamp' | 'read'>) => {
    const newNotification: Notification = {
      id: Date.now().toString(),
      timestamp: new Date(),
      read: false,
      ...notification
    }
    notifications.value.unshift(newNotification)
    
    // 限制通知数量
    if (notifications.value.length > 50) {
      notifications.value = notifications.value.slice(0, 50)
    }
  }

  const markNotificationAsRead = (id: string) => {
    const notification = notifications.value.find(n => n.id === id)
    if (notification) {
      notification.read = true
    }
  }

  const clearNotifications = () => {
    notifications.value = []
  }

  return {
    // 状态
    version,
    theme,
    sidebarCollapsed,
    loading,
    notifications,
    
    // 计算属性
    unreadNotifications,
    appTitle,
    
    // 动作
    applyTheme,
    initialize,
    toggleTheme,
    toggleSidebar,
    setLoading,
    addNotification,
    markNotificationAsRead,
    clearNotifications
  }
})