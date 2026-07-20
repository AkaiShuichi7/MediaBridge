"""
@description P115CloudService 实现模块
@responsibility 将 P115Client 封装为符合 CloudService 抽象接口的 115 网盘服务实现
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from loguru import logger

from app.services.cloud.base import CloudService
from app.schemas.cloud_types import CloudFile

if TYPE_CHECKING:
    from app.services.p115_client import P115Client


class P115CloudService(CloudService):
    """
    115 网盘云服务实现。

    将 P115Client 的底层 API 调用适配为 CloudService 抽象接口，
    所有返回的文件信息均规范化为 CloudFile 数据类。
    """

    def __init__(self, client: "P115Client") -> None:
        """
        初始化 P115CloudService。

        Args:
            client: P115Client 实例，负责与 115 网盘 API 通信
        """
        self._client = client

    async def list_files(self, dir_id: str) -> list:
        """
        列出指定目录下的所有文件和子目录。

        Args:
            dir_id: 目录的 115 网盘 ID（cid）

        Returns:
            CloudFile 对象列表
        """
        result = await self._client.list_directory(dir_id)
        items = result.get("data", [])
        cloud_files = [CloudFile.from_p115_dict(item) for item in items]
        logger.debug(f"列出目录 {dir_id} 完成，共 {len(cloud_files)} 个条目")
        return cloud_files

    async def move_file(self, file_id: str, target_dir_id: str) -> bool:
        """
        将文件移动到目标目录。

        Args:
            file_id: 被移动文件的 115 ID（fid）
            target_dir_id: 目标目录的 115 ID（cid）

        Returns:
            True 表示移动成功，False 表示失败
        """
        result = await self._client.move_file(file_id, target_dir_id)
        success = bool(result.get("state", False))
        if success:
            logger.debug(f"文件 {file_id} 已移动至目录 {target_dir_id}")
        else:
            logger.warning(f"移动文件 {file_id} 至 {target_dir_id} 失败: {result}")
        return success

    async def rename_file(self, file_id: str, new_name: str) -> bool:
        """
        重命名文件或目录。

        Args:
            file_id: 目标文件的 115 ID（fid）
            new_name: 新文件名（不含路径）

        Returns:
            True 表示重命名成功，False 表示失败
        """
        result = await self._client.rename_file(file_id, new_name)
        success = bool(result.get("state", False))
        if success:
            logger.debug(f"文件 {file_id} 已重命名为 {new_name}")
        else:
            logger.warning(f"重命名文件 {file_id} 为 {new_name} 失败: {result}")
        return success

    async def create_directory(self, parent_id: str, name: str) -> str:
        """
        在指定父目录下创建新目录。

        使用 fs_makedirs_app 接口按完整路径创建目录。
        注意：115 API 不支持直接按父目录 ID + 名称创建，此方法暂未支持。

        Args:
            parent_id: 父目录的 115 ID（cid）
            name: 新目录名称

        Returns:
            新创建目录的 115 ID

        Raises:
            NotImplementedError: 当前版本不支持通过父目录 ID 直接创建目录
        """
        # 115 API 的 fs_makedirs_app 需要完整路径字符串，无法仅凭 parent_id+name 构造
        # 如需创建，应通过 get_path_id(path, mkdir=True) 完成
        raise NotImplementedError(
            "创建目录功能请通过 get_path_id(path, mkdir=True) 实现，"
            "115 API 不支持直接按父目录 ID 创建"
        )

    async def get_path_id(
        self, path: str, mkdir: bool = True, library_name: str = "default"
    ) -> Optional[str]:
        return await self._client.get_path_id(
            path, mkdir=mkdir, library_name=library_name
        )

    async def add_offline_task(self, urls: list, save_dir_id: str) -> dict:
        """
        添加离线下载任务。

        Args:
            urls: 待下载链接列表（magnet 或 HTTP 直链），当前仅使用第一个
            save_dir_id: 下载完成后保存到的目录 ID

        Returns:
            包含任务结果信息的字典
        """
        if not urls:
            logger.warning("添加离线任务时 urls 列表为空")
            return {"state": False, "error": "urls 列表为空"}
        # 115 API 每次只能添加一个 URL
        result = await self._client.add_offline_task(urls[0], save_dir_id)
        logger.debug(f"已添加离线任务: {urls[0][:60]}... -> 目录 {save_dir_id}")
        return result

    async def get_offline_tasks(self) -> list:
        """
        获取当前所有离线下载任务列表。

        Returns:
            任务信息字典组成的列表
        """
        result = await self._client.get_offline_tasks()
        tasks = (result.get("tasks") or result.get("data")) if isinstance(result, dict) else None
        tasks = tasks or []
        logger.debug(f"获取到 {len(tasks)} 个离线任务")
        return tasks

    async def delete_offline_task(self, task_hash: str) -> bool:
        """
        删除指定的离线下载任务。

        Args:
            task_hash: 任务唯一哈希标识（info_hash）

        Returns:
            True 表示删除成功，False 表示失败
        """
        result = await self._client.delete_offline_task(task_hash)
        success = bool(result.get("state", False))
        if success:
            logger.debug(f"离线任务 {task_hash} 已删除")
        else:
            logger.warning(f"删除离线任务 {task_hash} 失败: {result}")
        return success

    async def list_directory(self, dir_id: str) -> dict:
        """
        获取目录的原始 API 数据（供内部逻辑使用）。

        Args:
            dir_id: 目录的云盘 ID

        Returns:
            包含 data 字段的 API 响应字典
        """
        result = await self._client.list_directory(dir_id)
        logger.debug(f"原始列目录 {dir_id}，返回 {len(result.get('data', []))} 条")
        return result

    async def delete_file(self, file_id: str) -> bool:
        """
        删除云盘中的指定文件。

        Args:
            file_id: 被删除文件的云盘 ID

        Returns:
            True 表示删除成功，False 表示失败
        """
        result = await self._client.delete_file(file_id)
        if isinstance(result, dict):
            success = bool(result.get("state", False))
        else:
            success = bool(result)
        if success:
            logger.debug(f"文件 {file_id} 已删除")
        else:
            logger.warning(f"删除文件 {file_id} 失败: {result}")
        return success
