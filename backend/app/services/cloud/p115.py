"""115 implementation of the application cloud-service contract."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from loguru import logger

from app.schemas.cloud_types import CloudFile
from app.services.cloud.base import CloudService

if TYPE_CHECKING:
    from app.services.p115_client import P115Client


class P115CloudService(CloudService):
    """Normalize the 115 SDK wrapper for the rest of the application."""

    def __init__(self, client: "P115Client") -> None:
        self._client = client

    async def list_files(self, dir_id: str) -> list[CloudFile]:
        result = await self._client.list_directory(dir_id)
        return [CloudFile.from_p115_dict(item) for item in result.get("data", [])]

    async def move_file(self, file_id: str, target_dir_id: str) -> bool:
        result = await self._client.move_file(file_id, target_dir_id)
        return bool(result.get("state", False))

    async def rename_file(self, file_id: str, new_name: str) -> bool:
        result = await self._client.rename_file(file_id, new_name)
        return bool(result.get("state", False))

    async def get_path_id(
        self, path: str, mkdir: bool = True, library_name: str = "default"
    ) -> Optional[str]:
        return await self._client.get_path_id(
            path, mkdir=mkdir, library_name=library_name
        )

    async def add_offline_task(self, url: str, save_dir_id: str) -> dict:
        return await self._client.add_offline_task(url, save_dir_id)

    async def get_offline_tasks(self) -> list[dict]:
        result = await self._client.get_offline_tasks()
        if not isinstance(result, dict):
            logger.warning("115 task list returned a non-dict response")
            return []
        return result.get("tasks") or result.get("data") or []

    async def get_offline_task(self, task_hash: str) -> Optional[dict]:
        return await self._client.get_task_status(task_hash)

    async def delete_offline_task(self, task_hash: str) -> bool:
        result = await self._client.delete_offline_task(task_hash)
        return bool(result.get("state", False))

    async def list_directory(self, dir_id: str) -> dict:
        return await self._client.list_directory(dir_id)

    async def delete_file(self, file_id: str) -> bool:
        result = await self._client.delete_file(file_id)
        return bool(result.get("state", False)) if isinstance(result, dict) else bool(result)
