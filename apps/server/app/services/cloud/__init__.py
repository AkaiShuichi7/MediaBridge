"""
@description 云服务模块初始化
@responsibility 导出 CloudService 抽象基类和 P115CloudService 实现类
"""

from app.services.cloud.base import CloudService
from app.services.cloud.p115 import P115CloudService

__all__ = ["CloudService", "P115CloudService"]
