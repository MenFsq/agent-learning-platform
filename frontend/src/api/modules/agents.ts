import httpClient from '../httpClient';

export const agentAPI = {
  // 获取所有Agent
  getAgents: () => httpClient.get('/api/v1/agents'),

  // 获取单个Agent
  getAgent: (id: string) => httpClient.get(`/api/v1/agents/${id}`),

  // 创建Agent
  createAgent: (data: {
    name: string
    description: string
    type: string
    model: string
    temperature?: number
    memory?: boolean
    tools?: string[]
  }) => httpClient.post('/api/v1/agents', data),

  // 更新Agent
  updateAgent: (id: string, data: {
    name?: string
    description?: string
    type?: string
    model?: string
    temperature?: number
    memory?: boolean
    tools?: string[]
  }) => httpClient.put(`/api/v1/agents/${id}`, data),

  // 删除Agent
  deleteAgent: (id: string) => httpClient.delete(`/api/v1/agents/${id}`),

  // 启动Agent
  startAgent: (id: string) => httpClient.post(`/api/v1/agents/${id}/start`),

  // 停止Agent
  stopAgent: (id: string) => httpClient.post(`/api/v1/agents/${id}/stop`),

  // 与Agent交互
  interactWithAgent: (id: string, message: string) =>
    httpClient.post(`/api/v1/agents/${id}/interact`, { message })
};