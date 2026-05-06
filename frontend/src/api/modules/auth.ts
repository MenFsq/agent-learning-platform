import httpClient from '../httpClient';

export const authAPI = {
  // 用户注册
  register: (data: { username: string; email: string; password: string; full_name?: string }) =>
    httpClient.post('/auth/register', data),

  // 用户登录
  login: (data: { username: string; password: string }) =>
    httpClient.post('/auth/login/json', data),

  // 获取当前用户信息
  getCurrentUser: () => httpClient.get('/auth/me'),

  // 刷新token
  refreshToken: () => httpClient.post('/auth/refresh')
};