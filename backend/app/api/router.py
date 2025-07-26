from fastapi import APIRouter
from .endpoints import openlist, emby

api_router = APIRouter()

# 包含各个模块的路由
api_router.include_router(openlist.router, prefix="/openlist", tags=["openlist"])
api_router.include_router(emby.router, prefix="/emby", tags=["emby"])
