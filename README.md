# MediaBridge

MediaBridge 是一个连接 OpenList 和 Emby 的工具，旨在简化和自动化媒体的下载、整理和入库流程。

## 技术栈

- **后端**: Python + FastAPI
- **前端**: Vue.js + TypeScript

## 如何运行

### 后端

1. 进入后端目录: `cd backend`
2. 激活虚拟环境: `source .venv/bin/activate`
3. 启动开发服务器: `cd backend && uvicorn app.main:app --reload`

### 前端

1. 进入前端目录: `cd frontend`
2. 安装依赖: `npm install`
3. 启动开发服务器: `npm run dev`
