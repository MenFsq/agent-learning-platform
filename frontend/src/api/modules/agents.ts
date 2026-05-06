import httpClient from '../httpClient';

export const agentAPI = {
  // 获取所有Agent
  getAgents: () => httpClient.get('/agents'),

  // 获取单个Agent
  getAgent: (id: string) => httpClient.get(`/agents/${id}`),

  // 创建Agent
  createAgent: (data: {
    name: string
    description: string
    type: string
    model: string
    temperature?: number
    memory?: boolean
    tools?: string[]
  }) => httpClient.post('/agents', data),

  // 更新Agent
  updateAgent: (id: string, data: {
    name?: string
    description?: string
    type?: string
    model?: string
    temperature?: number
    memory?: boolean
    tools?: string[]
  }) => httpClient.put(`/agents/${id}`, data),

  // 删除Agent
  deleteAgent: (id: string) => httpClient.delete(`/agents/${id}`),

  // 启动Agent
  startAgent: (id: string) => httpClient.post(`/agents/${id}/start`),

  // 停止Agent
  stopAgent: (id: string) => httpClient.post(`/agents/${id}/stop`),

  // 与Agent对话
  chatWithAgent: (id: string, message: string) =>
    httpClient.post(`/agents/${id}/chat`, { message }),

  // 获取对话历史
  getConversations: (id: string, limit: number = 50) =>
    httpClient.get(`/agents/${id}/conversations`, { params: { limit } }),

  // 清空对话历史
  clearConversations: (id: string) =>
    httpClient.delete(`/agents/${id}/conversations`),

  // 与Agent交互（兼容旧接口）
  interactWithAgent: (id: string, message: string) =>
    httpClient.post(`/agents/${id}/chat`, { message })
};