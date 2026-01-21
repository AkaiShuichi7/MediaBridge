# MediaBridge (MediaBridge)

MediaBridge 是一个轻量级的媒体桥接工具，采用前后端分离架构，旨在提供更便捷、更安全的离线下载管理和文件整理体验。

## ✨ 核心特性

*   **轻量级架构**: Python Flask 后端 + Vue3 前端，资源占用低。
*   **安全防风控**: 内置 Web/App 双端 API 轮询机制，模拟真实用户行为，降低封号风险。
*   **原生体验**: 支持 PWA (Progressive Web App)，可安装到手机或电脑桌面，全屏运行。
*   **智能管理**: 支持磁力链接离线下载、文件重命名/移动等基础操作。

## 🛠️ 技术栈

*   **前端**: Vue 3, Vite, Vant UI, Pinia, TypeScript
*   **后端**: Python 3, Flask, SQLAlchemy, APScheduler
*   **核心库**: [p115client](https://github.com/ChenyangGao/p115client) (感谢 ChenyangGao 大佬)
*   **数据库**: SQLite

## 🚀 快速开始

### 1. 环境要求
*   Python 3.8+
*   Node.js 18+

### 2. 启动后端

```bash
# 假设你在项目根目录 MediaBridge/
# Windows 激活虚拟环境 (确保你已在 backend/.venv 创建了虚拟环境)
.\backend\.venv\Scripts\activate

# 安装依赖
pip install -r backend/requirements.txt

# 启动服务 (默认端口 5001)
python backend/run.py
```

### 3. 启动前端

```bash
cd frontend
# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

访问 `http://localhost:3000` 即可开始使用。

## 📝 待办事项 (Todo)

- [ ] 用户 Cookie 导入与验证
- [ ] 离线下载任务添加与进度监控
- [ ] 文件浏览与基础管理
- [ ] 自动化任务调度

## 📄 开源协议

MIT License
