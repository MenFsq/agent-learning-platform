import axios from 'axios';
import router from '@/router';

const configuredBaseURL = (import.meta.env.VITE_API_BASE_URL || '').trim();
const normalizedBaseURL = configuredBaseURL.replace(/\/$/, '');

const httpClient = axios.create({
  baseURL: normalizedBaseURL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 请求拦截器
httpClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
httpClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response && error.response.status === 401) {
      // 认证失败
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      
      // 使用 router 实例进行跳转
      if (router.currentRoute.value.path !== '/login') {
        router.push('/login');
      }
    }
    return Promise.reject(error);
  }
);

export default httpClient;