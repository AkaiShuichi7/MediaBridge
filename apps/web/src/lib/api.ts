// @ts-ignore
import axios from 'axios'

// 重要：使用相对路径，通过 Vite 代理到后端，避免 CORS 错误
// 代理配置在 vite.config.ts 中：/api -> http://localhost:8000
export const api = axios.create({
  baseURL: '',  // 使用相对路径，通过 Vite 代理
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add response interceptor for error handling
api.interceptors.response.use(
  (response: any) => response,
  (error: any) => {
    return Promise.reject(error)
  }
)
