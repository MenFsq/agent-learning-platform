import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8003',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 从localStorage获取token
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response?.status === 401) {
      // 未授权，清除token并跳转到登录页
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// API方法
export const authAPI = {
  // 用户注册
  register: (data: { username: string; email: string; password: string; full_name?: string }) =>
    api.post('/api/v1/auth/register', data),

  // 用户登录
  login: (data: { username: string; password: string }) =>
    api.post('/api/v1/auth/login', data),

  // 获取当前用户信息
  getCurrentUser: () => api.get('/api/v1/auth/me'),

  // 刷新token
  refreshToken: () => api.post('/api/v1/auth/refresh')
}

export const projectAPI = {
  // 获取所有项目
  getProjects: () => api.get('/api/v1/projects'),

  // 获取用户项目
  getMyProjects: () => api.get('/api/v1/projects/my'),

  // 获取单个项目
  getProject: (id: number) => api.get(`/api/v1/projects/${id}`),

  // 创建项目
  createProject: (data: { name: string; description?: string; is_public?: boolean }) =>
    api.post('/api/v1/projects', data),

  // 更新项目
  updateProject: (id: number, data: { name?: string; description?: string; is_public?: boolean ;status?: string}) =>
    api.put(`/api/v1/projects/${id}`, data),

  // 删除项目
  deleteProject: (id: number) => api.delete(`/api/v1/projects/${id}`)
}

export const agentAPI = {
  // 获取所有Agent
  getAgents: () => api.get('/api/v1/agents'),

  // 获取单个Agent
  getAgent: (id: string) => api.get(`/api/v1/agents/${id}`),

  // 创建Agent
  createAgent: (data: {
    name: string
    description: string
    type: string
    model: string
    temperature?: number
    memory?: boolean
    tools?: string[]
  }) => api.post('/api/v1/agents', data),

  // 更新Agent
  updateAgent: (id: string, data: {
    name?: string
    description?: string
    type?: string
    model?: string
    temperature?: number
    memory?: boolean
    tools?: string[]
  }) => api.put(`/api/v1/agents/${id}`, data),

  // 删除Agent
  deleteAgent: (id: string) => api.delete(`/api/v1/agents/${id}`),

  // 启动Agent
  startAgent: (id: string) => api.post(`/api/v1/agents/${id}/start`),

  // 停止Agent
  stopAgent: (id: string) => api.post(`/api/v1/agents/${id}/stop`),

  // 与Agent交互
  interactWithAgent: (id: string, message: string) =>
    api.post(`/api/v1/agents/${id}/interact`, { message })
}

// 健康检查
export const healthAPI = {
  checkHealth: () => api.get('/health')
}

export default api