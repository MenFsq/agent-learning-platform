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
  const theme = ref<'light' | 'dark'>('light')
  const sidebarCollapsed = ref(false)
  const loading = ref(false)
  const notifications = ref<Notification[]>([])

  // 计算属性
  const unreadNotifications = computed(() => 
    notifications.value.filter(n => !n.read).length
  )

  const appTitle = computed(() => 'Agent Learning Platform')

  // 动作
  const initialize = () => {
    console.log('App initialized')
    // 从localStorage恢复状态
    const savedTheme = localStorage.getItem('theme')
    if (savedTheme === 'light' || savedTheme === 'dark') {
      theme.value = savedTheme
    }
  }

  const toggleTheme = () => {
    theme.value = theme.value === 'light' ? 'dark' : 'light'
    localStorage.setItem('theme', theme.value)
    document.documentElement.setAttribute('data-theme', theme.value)
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
    initialize,
    toggleTheme,
    toggleSidebar,
    setLoading,
    addNotification,
    markNotificationAsRead,
    clearNotifications
  }
})