<script setup lang="ts">
import { ref } from 'vue';

const magnetLink = ref('');

const onSubmit = () => {
  // TODO: Call API
  console.log('Submit:', magnetLink.value);
};
</script>

<template>
  <div class="page-content">
    <van-nav-bar title="离线下载" />
    
    <div class="input-area">
      <van-cell-group inset>
        <van-field
          v-model="magnetLink"
          rows="2"
          autosize
          label="链接"
          type="textarea"
          placeholder="粘贴磁力链接/电驴/HTTP链接"
          clearable
        />
      </van-cell-group>
      <div style="margin: 16px;">
        <van-button round block type="primary" native-type="submit" @click="onSubmit">
          添加任务
        </van-button>
      </div>
    </div>

    <van-empty description="暂无下载任务" />
  </div>
</template>

<style scoped>
.page-content {
  padding-top: 0;
}
.input-area {
  margin-top: 20px;
}
</style>
