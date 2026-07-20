/**
 * @description React Query 全局客户端配置
 * @responsibility 定义查询默认选项（缓存策略、重试次数等）
 */
import { QueryClient } from '@tanstack/react-query'

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      // 30 秒内不重新请求
      staleTime: 30 * 1000,
      // 失败最多重试 2 次
      retry: 2,
      // 窗口聚焦不自动刷新
      refetchOnWindowFocus: false,
    },
  },
})
