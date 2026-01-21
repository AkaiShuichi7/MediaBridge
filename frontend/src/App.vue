<script setup lang="ts">
/**
 * @description 根组件 Layout
 * @responsibility 定义应用的全局布局，包括底部的 Tabbar 导航
 */
import { ref } from 'vue';
import { RouterView } from 'vue-router';

// 当前选中的标签页索引
const active = ref(0);
</script>

<template>
  <div class="app-container">
    <!-- 路由视图渲染区域 -->
    <RouterView />
    
    <!-- 底部导航栏: 路由模式 (route) -->
    <van-tabbar v-model="active" route>
      <van-tabbar-item replace to="/" icon="down">离线下载</van-tabbar-item>
      <van-tabbar-item replace to="/files" icon="folder-o">文件管理</van-tabbar-item>
      <van-tabbar-item replace to="/settings" icon="setting-o">设置</van-tabbar-item>
    </van-tabbar>
  </div>
</template>

<style scoped>
.app-container {
  padding-bottom: 50px; /* 为底部 Tabbar 预留空间 */
  min-height: 100vh;
  background-color: #f7f8fa;
}
</style>
