# MediaBridge 前端

基于 React + Vite + TypeScript + TailwindCSS 的 Web 应用。

## 特性

- React 18 + TypeScript
- Vite 构建 + HMR
- TailwindCSS v4
- PWA 支持
- Axios 请求库
- React Query 数据管理

## 开发

```bash
npm install
npm run dev
```

访问 http://localhost:5173

## Docker 部署

### 单独运行

```bash
# 拉取镜像
docker pull akaishuichiw/media-bridge-frontend:latest

# 运行容器
docker run -d -p 8080:80 --name media-bridge-frontend \
  akaishuichiw/media-bridge-frontend:latest
```

### Docker Compose（推荐）

```bash
# 启动前后端服务
docker-compose up -d

# 查看服务状态
docker-compose ps
```

访问 http://localhost:8080

## API 代理配置

| 环境 | API 地址 | 代理配置 |
|------|----------|----------|
| 本地开发 | Vite 代理到 localhost:8000 | vite.config.ts |
| Docker | Nginx 代理到 backend:8000 | nginx.conf |

本地开发时，前端通过 Vite 代理 `/api` 请求到 `http://localhost:8000`。

Docker 部署时，Nginx 代理 `/api` 请求到 `backend` 服务（Docker Compose 服务名）。

## 项目结构

```
frontend/
├── src/
│   ├── components/     # 组件
│   ├── pages/          # 页面
│   ├── hooks/          # React Hooks
│   ├── lib/            # 工具库 (axios)
│   └── types/          # TypeScript 类型
├── public/             # 静态资源
├── nginx.conf         # Nginx 配置
└── Dockerfile         # Docker 构建文件
```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```
