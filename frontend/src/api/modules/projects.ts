import httpClient from '../httpClient';

export const projectAPI = {
  // 获取所有项目
  getProjects: () => httpClient.get('/projects/'),

  // 获取用户项目
  getMyProjects: () => httpClient.get('/projects/my/'),

  // 获取单个项目
  getProject: (id: number) => httpClient.get(`/projects/${id}/`),

  // 创建项目
  createProject: (data: { name: string; description?: string; is_public?: boolean }) =>
    httpClient.post('/projects/', data),

  // 更新项目
  updateProject: (id: number, data: { name?: string; description?: string; is_public?: boolean ;status?: string}) =>
    httpClient.put(`/projects/${id}/`, data),

  // 删除项目
  deleteProject: (id: number) => httpClient.delete(`/projects/${id}/`)
};