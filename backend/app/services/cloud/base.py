"""Provider-neutral cloud storage operations used by the application."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional


class CloudService(ABC):
    """The application-level contract for a cloud storage provider.

    The contract exposes only operations that every supported provider can
    genuinely implement. Directory creation is performed through
    :meth:`get_path_id` because the 115 API is path-based.
    """

    @abstractmethod
    async def list_files(self, dir_id: str) -> list:
        """Return normalized files in a directory."""

    @abstractmethod
    async def move_file(self, file_id: str, target_dir_id: str) -> bool:
        """Move a file and report whether it succeeded."""

    @abstractmethod
    async def rename_file(self, file_id: str, new_name: str) -> bool:
        """Rename a file and report whether it succeeded."""

    @abstractmethod
    async def get_path_id(
        self, path: str, mkdir: bool = True, library_name: str = "default"
    ) -> Optional[str]:
        """Resolve a path, optionally creating missing directories."""

    @abstractmethod
    async def add_offline_task(self, url: str, save_dir_id: str) -> dict:
        """Create one offline download task."""

    @abstractmethod
    async def get_offline_tasks(self) -> list[dict]:
        """Return all currently visible offline tasks."""

    @abstractmethod
    async def get_offline_task(self, task_hash: str) -> Optional[dict]:
        """Return one offline task, or ``None`` if it does not exist."""

    @abstractmethod
    async def delete_offline_task(self, task_hash: str) -> bool:
        """Delete an offline task."""

    @abstractmethod
    async def list_directory(self, dir_id: str) -> dict:
        """Return the provider's raw directory response for organizer logic."""

    @abstractmethod
    async def delete_file(self, file_id: str) -> bool:
        """Delete a file and report whether it succeeded."""
