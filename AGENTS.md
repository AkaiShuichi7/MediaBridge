# MediaBridge 项目开发指南 (AGENTS.md)

本文件为 MediaBridge 项目的 AI 助手和开发人员提供特定于本项目的技术栈说明及操作指南。
关于全局通用的代码规范（如语言设定、Git 提交格式、通用代码质量原则），请直接遵循全局 `AGENTS.md` 规则，本文档不再赘述。

## 1. 项目概览
MediaBridge 是一个基于 115 网盘 API 的媒体桥接助手，采用前后端分离架构。
- **后端**: Flask 提供 RESTful API，处理 115 核心逻辑。
- **前端**: Vue 3 + Vant UI 构建的移动端优先 Web 应用，支持 PWA。

## 2. 技术栈
### 后端 (Backend)
- **核心库**: `p115client` (核心 115 交互库)
- **运行环境**: 建议使用 `.venv` 虚拟环境
- **任务调度**: APScheduler

### 前端 (Frontend)
- **UI 组件库**: Vant 4
- **状态管理**: Pinia
- **特性**: 支持 PWA (vite-plugin-pwa)

## 3. 常用命令

### 后端管理
- **激活环境 (Windows)**: `.\backend\.venv\Scripts\activate`
- **安装依赖**: `pip install -r backend/requirements.txt`
- **启动服务**: `python backend/run.py` (默认端口 5001)

### 前端管理
- **开发运行**: `npm run dev` (访问 http://localhost:3000)
- **构建项目**: `npm run build`

## 4. 专项开发规范

### 4.1 后端规范 (Python/115)
- **115 交互 (核心)**: 
  - 必须通过 `CookieOnly115Manager` 类进行调用，严禁直接实例化 `P115Client`。
  - **双端轮询**: 必须同时初始化 Web 和 App (ios/android) 客户端，并在请求时进行轮询以降低风控风险。
  - **速率限制**: 在进行离线下载或文件操作前，必须添加随机延迟 (`time.sleep(random.uniform(2.0, 5.0))`)。
- **错误处理**: 显式捕捉异常，特别是针对 115 的风控（如错误码 911 验证码）应有明确的记录或提示。

### 4.2 前端规范 (Vue/Vant)
- **UI 开发**: 优先使用 Vant 组件，保持移动端体验一致性。
- **状态管理**: 业务逻辑尽量封装在 Pinia Store 中，保持组件简洁。

## 5. 架构说明
- **跨域处理**: 前端 Vite 配置了代理，将 `/api` 请求转发至后端 `http://127.0.0.1:5001`。
- **数据库**: 数据存储在 `backend/instance/app.db`。
- **PWA**: 配置文件位于 `frontend/vite.config.ts` 中的 `VitePWA` 部分。

## 6. 特别注意事项
- **安全**: 严禁将包含真实 Cookie 的配置文件或数据库文件提交至 Git。
- **风控**: 模拟真实用户行为是本项目核心原则，开发新功能时务必考虑 API 调用频率。
