"""
@description 核心基础设施模块初始化
@responsibility 导出配置加载、应用容器和依赖注入提供者
"""

from app.core.config import load_config
from app.core.container import AppContainer
from app.core.dependencies import get_config, get_p115_client, get_cloud_service, get_task_monitor, get_file_organizer

__all__ = [
    "load_config",
    "AppContainer",
    "get_config",
    "get_p115_client",
    "get_cloud_service",
    "get_task_monitor",
    "get_file_organizer",
]
