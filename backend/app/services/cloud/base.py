"""
@description CloudService 抽象基类模块
@responsibility 定义云盘服务的统一抽象接口，供各云盘具体实现继承
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.cloud_types import CloudFile


class CloudService(ABC):
    """
    云盘服务抽象基类。

    所有云盘服务实现（如 P115CloudService）必须继承此类并实现全部抽象方法。
    方法返回的文件信息统一使用 CloudFile 数据类，实现细节由子类负责字段规范化。
    """

    @abstractmethod
    async def list_files(self, dir_id: str) -> list:
        """
        列出指定目录下的所有文件和子目录。

        Args:
            dir_id: 目录的云盘 ID

        Returns:
            CloudFile 对象列表，每个元素代表一个文件或目录
        """
        ...

    @abstractmethod
    async def move_file(self, file_id: str, target_dir_id: str) -> bool:
        """
        将文件移动到目标目录。

        Args:
            file_id: 被移动文件的云盘 ID
            target_dir_id: 目标目录的云盘 ID

        Returns:
            True 表示移动成功，False 表示失败
        """
        ...

    @abstractmethod
    async def rename_file(self, file_id: str, new_name: str) -> bool:
        """
        重命名文件或目录。

        Args:
            file_id: 目标文件的云盘 ID
            new_name: 新文件名（不含路径）

        Returns:
            True 表示重命名成功，False 表示失败
        """
        ...

    @abstractmethod
    async def create_directory(self, parent_id: str, name: str) -> str:
        """
        在指定父目录下创建新目录。

        Args:
            parent_id: 父目录的云盘 ID
            name: 新目录名称

        Returns:
            新创建目录的云盘 ID
        """
        ...

    @abstractmethod
    async def get_path_id(self, path: str, mkdir: bool = True) -> Optional[str]:
        """
        根据路径字符串获取对应的云盘目录 ID。

        Args:
            path: 目录路径，如 "/电影/动作" 或 "0" 表示根目录
            mkdir: 目录不存在时是否自动创建

        Returns:
            对应的云盘 ID，路径不存在时返回 None
        """
        ...

    @abstractmethod
    async def add_offline_task(self, urls: list, save_dir_id: str) -> dict:
        """
        添加离线下载任务。

        Args:
            urls: 待下载的链接列表（magnet 或 HTTP 直链）
            save_dir_id: 下载完成后保存到的目录 ID

        Returns:
            包含任务结果信息的字典
        """
        ...

    @abstractmethod
    async def get_offline_tasks(self) -> list:
        """
        获取当前所有离线下载任务列表。

        Returns:
            任务信息字典组成的列表
        """
        ...

    @abstractmethod
    async def delete_offline_task(self, task_hash: str) -> bool:
        """
        删除指定的离线下载任务。

        Args:
            task_hash: 任务的唯一哈希标识（通常为 info_hash）

        Returns:
            True 表示删除成功，False 表示失败
        """
        ...

    @abstractmethod
    async def list_directory(self, dir_id: str) -> dict:
        """
        列出指定目录的原始 API 数据（供内部逻辑使用）。

        Args:
            dir_id: 目录的云盘 ID

        Returns:
            包含 data 字段的 API 响应字典
        """
        ...

    @abstractmethod
    async def delete_file(self, file_id: str) -> bool:
        """
        删除云盘中的指定文件。

        Args:
            file_id: 被删除文件的云盘 ID

        Returns:
            True 表示删除成功，False 表示失败
        """
        ...
