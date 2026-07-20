"""
@description 缓存服务模块初始化
@responsibility 导出路径 ID 缓存服务，为上层服务提供统一的缓存访问接口
"""

from app.services.cache.path_cache import PathIdCacheService

__all__ = ["PathIdCacheService"]
