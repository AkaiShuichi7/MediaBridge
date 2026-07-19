# MediaBridge

MediaBridge 是一个用于管理 115 离线下载和媒体文件整理的 Web 应用。仓库包含 React 前端与 FastAPI 后端，并提供一个可直接部署的 Docker 镜像。

## 部署

1. 创建配置与持久化目录：

   ```bash
   cp backend/config.example.yaml config.yaml
   mkdir -p db logs
   ```

2. 编辑 `config.yaml`，填写实际的 115 Cookies 和媒体库路径。

3. 运行镜像（默认镜像名为 `akaishuichiw/mediabridge:latest`）：

   ```bash
   docker compose up -d
   ```

   如 Docker Hub 用户名或镜像名不同，请设置 `IMAGE_NAME`：

   ```bash
   IMAGE_NAME=your-dockerhub-user/mediabridge:latest docker compose up -d
   ```

部署完成后，打开 `http://<host>:8080`。FastAPI 文档位于 `http://<host>:8080/docs`。

## Docker Hub 自动发布

推送到 `main` 或推送 `v*` 标签时，GitHub Actions 会构建并推送单一镜像。请先在仓库的 **Settings → Secrets and variables → Actions** 中创建：

- `DOCKERHUB_USERNAME`：Docker Hub 用户名。
- `DOCKERHUB_TOKEN`：在 Docker Hub 创建的 Access Token；不要使用账户密码。

镜像将发布为 `${DOCKERHUB_USERNAME}/mediabridge`，`main` 分支会同时更新 `latest` 标签。

## 本地开发

后端在 `backend/`，前端在 `frontend/`。前端开发服务器会把 `/api` 转发到 `http://localhost:8000`。

```bash
cd backend
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m uvicorn main:app --reload
```

另开一个终端：

```bash
cd frontend
npm ci
npm run dev
```
