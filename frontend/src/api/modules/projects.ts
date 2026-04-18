import httpClient from '../httpClient';

export const projectAPI = {
  // 获取所有项目
  getProjects: () => httpClient.get('/api/v1/projects'),

  // 获取用户项目
  getMyProjects: () => httpClient.get('/api/v1/projects/my'),

  // 获取单个项目
  getProject: (id: number) => httpClient.get(`/api/v1/projects/${id}`),

  // 创建项目
  createProject: (data: { name: string; description?: string; is_public?: boolean }) =>
    httpClient.post('/api/v1/projects', data),

  // 更新项目
  updateProject: (id: number, data: { name?: string; description?: string; is_public?: boolean ;status?: string}) =>
    httpClient.put(`/api/v1/projects/${id}`, data),

  // 删除项目
  deleteProject: (id: number) => httpClient.delete(`/api/v1/projects/${id}`)
};