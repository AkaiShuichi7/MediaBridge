# --- Stage 1: Build Frontend ---
FROM node:18-alpine AS frontend-builder

# 设置工作目录
WORKDIR /app/frontend

# 复制 package.json 和 package-lock.json
COPY frontend/package*.json ./

# 安装依赖
RUN npm install

# 复制所有前端代码
COPY frontend/ ./

# 构建生产版本的前端应用
RUN npm run build

# --- Stage 2: Final Application ---
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 创建一个非 root 用户来运行应用，更安全
RUN addgroup --system app && adduser --system --group app

# 复制后端的依赖文件
COPY backend/requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 从前端构建阶段复制编译好的静态文件
COPY --from=frontend-builder /app/frontend/dist /app/backend/static

# 复制后端的代码
COPY backend/ /app/backend/

# 确保 app 用户拥有所有权
RUN chown -R app:app /app

# 切换到非 root 用户
USER app

# 暴露端口
EXPOSE 8000

# 设置工作目录为 backend
WORKDIR /app/backend

# 容器启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
