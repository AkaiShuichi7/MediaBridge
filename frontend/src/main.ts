/**
 * @description 前端入口文件
 * @responsibility 初始化 Vue 应用实例，挂载 Pinia、Router 和 Vant UI 库
 */

import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Vant from 'vant'
import 'vant/lib/index.css'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia()) // 状态管理
app.use(router)        // 路由
app.use(Vant)          // UI 组件库

app.mount('#app')
