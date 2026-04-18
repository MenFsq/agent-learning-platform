import httpClient from '../httpClient';

export const authAPI = {
  // 用户注册
  register: (data: { username: string; email: string; password: string; full_name?: string }) =>
    httpClient.post('/api/v1/auth/register', data),

  // 用户登录
  login: (data: { username: string; password: string }) =>
    httpClient.post('/api/v1/auth/login', data),

  // 获取当前用户信息
  getCurrentUser: () => httpClient.get('/api/v1/auth/me'),

  // 刷新token
  refreshToken: () => httpClient.post('/api/v1/auth/refresh')
};