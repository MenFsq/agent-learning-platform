import httpClient from '../httpClient';

export const healthAPI = {
  checkHealth: () => httpClient.get('/health')
};