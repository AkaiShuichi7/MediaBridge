/**
 * @description Vite 构建配置文件
 * @responsibility 配置 Vue 插件、PWA 生成规则以及 API 反向代理
 */

import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA } from 'vite-plugin-pwa'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    // PWA 插件配置
    VitePWA({
      registerType: 'autoUpdate', // 检测到新版本时自动更新 Service Worker
      includeAssets: ['favicon.ico', 'apple-touch-icon.png', 'masked-icon.svg'],
      manifest: {
        name: 'MediaBridge',
        short_name: 'MediaBridge',
        description: 'MediaBridge 媒体桥接工具',
        theme_color: '#ffffff',
        background_color: '#ffffff',
        display: 'standalone', // 独立应用模式，隐藏浏览器 UI
        icons: [
          {
            src: 'pwa-192x192.png',
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: 'pwa-512x512.png',
            sizes: '512x512',
            type: 'image/png'
          }
        ]
      }
    })
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    host: '0.0.0.0', // 允许局域网访问
    port: 3000,
    // API 反向代理配置
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5001', // 转发到后端 Flask 服务
        changeOrigin: true
      }
    }
  }
})
