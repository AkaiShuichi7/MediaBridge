<template>
  <div>
    <van-nav-bar title="设置" />
    <van-cell-group title="账号信息">
      <van-cell title="昵称" value="未登录" />
      <van-cell title="VIP等级" value="-" />
    </van-cell-group>
    
    <van-cell-group title="系统设置" style="margin-top: 20px;">
      <van-cell title="导入 Cookie" is-link />
      <van-cell title="关于 MediaBridge" value="v0.1.0" />
    </van-cell-group>
  </div>
</template>
