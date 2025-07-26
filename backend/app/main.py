from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .api.router import api_router

app = FastAPI(title="MediaBridge API")

# 包含所有 API 路由
app.include_router(api_router, prefix="/api")

# 挂载静态文件目录，用于托管前端应用
# 注意：在新的结构中，static 目录应该位于 app 目录的上一级，即 backend/static
# 我们需要在 Dockerfile 中调整复制路径，或者在这里调整路径
# 为了简单起见，我们假设 static 目录在 app 目录的同级
app.mount("/", StaticFiles(directory="../static", html=True), name="static")
