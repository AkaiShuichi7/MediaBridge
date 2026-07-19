"""
@description 路径 ID 缓存服务模块
@responsibility 提供路径与 115 网盘目录 ID 之间的缓存映射，支持 UPSERT、查询、失效和清理操作
"""

import re
import time
from typing import Optional

from loguru import logger

# 缓存默认过期时间（秒），与 p115_client 保持一致
from app.services.p115_client import CACHE_TTL_SECONDS


class PathIdCacheService:
    """
    路径 ID 缓存服务。

    将路径（如 /云下载/电影/动作）与 115 网盘目录 ID 的对应关系
    持久化到 SQLite 数据库，减少重复的网络 API 调用。
    """

    def _normalize_path(self, path: str) -> str:
        """
        规范化路径为缓存 key。

        Args:
            path: 原始路径字符串

        Returns:
            str: 规范化后的路径，以 / 开头
        """
        if not path or path == "/":
            return "/"
        parts = [p for p in path.strip("/").split("/") if p]
        return "/" + "/".join(parts)

    def _is_temp_directory(self, path: str) -> bool:
        """
        判断路径是否是临时目录（如番号目录）。

        临时目录特征：路径最后一级匹配番号模式（大写字母 + 横杠 + 数字），
        如 MUDR-359、ABP-123、SSIS-001。

        Args:
            path: 完整路径

        Returns:
            bool: True 表示是临时目录
        """
        last_part = path.rsplit("/", 1)[-1]
        is_temp = bool(re.match(r"^[A-Z]+-\d+$", last_part))
        if is_temp:
            logger.debug(f"检测到临时目录: {last_part}")
        return is_temp

    async def get_cached_path_id(self, library_name: str, path: str) -> Optional[int]:
        """
        从缓存读取路径对应的目录 ID（读时过滤过期记录）。

        Args:
            library_name: 媒体库名称
            path: 目录路径

        Returns:
            Optional[int]: 缓存的目录 ID，未命中或已过期时返回 None
        """
        from app.core.database import get_session
        from app.models.path_id_cache import PathIdCache
        from sqlalchemy import select

        normalized_path = self._normalize_path(path)
        now = int(time.time())

        async with get_session() as session:
            result = await session.execute(
                select(PathIdCache.path_id).where(
                    PathIdCache.library_name == library_name,
                    PathIdCache.path == normalized_path,
                    PathIdCache.expires_at > now,
                )
            )
            row = result.scalar_one_or_none()
            if row is not None:
                logger.debug(f"缓存命中: {library_name}:{normalized_path} -> {row}")
            return row if row is not None else None

    async def set_cached_path_id(
        self,
        library_name: str,
        path: str,
        path_id: int,
        ttl_seconds: int = CACHE_TTL_SECONDS,
    ) -> None:
        """
        写入路径 ID 缓存（UPSERT，并发安全）。

        Args:
            library_name: 媒体库名称
            path: 目录路径
            path_id: 对应的 115 目录 ID
            ttl_seconds: 缓存过期时间（秒），默认 600 秒
        """
        from app.core.database import get_session
        from sqlalchemy import text

        normalized_path = self._normalize_path(path)
        now = int(time.time())
        expires_at = now + ttl_seconds

        async with get_session() as session:
            await session.execute(
                text("""
                INSERT INTO path_id_cache
                (library_name, path, path_id, expires_at, hit_count, created_at, updated_at)
                VALUES (:library_name, :path, :path_id, :expires_at, 0, :now, :now)
                ON CONFLICT(library_name, path) DO UPDATE SET
                    path_id = excluded.path_id,
                    expires_at = excluded.expires_at,
                    updated_at = excluded.updated_at
                """),
                {
                    "library_name": library_name,
                    "path": normalized_path,
                    "path_id": path_id,
                    "expires_at": expires_at,
                    "now": now,
                },
            )
            await session.commit()
        logger.debug(
            f"缓存写入: {library_name}:{normalized_path} -> {path_id} (TTL={ttl_seconds}s)"
        )

    async def invalidate_cache(self, library_name: str, path: str) -> None:
        """
        使指定路径的缓存失效（直接删除记录）。

        Args:
            library_name: 媒体库名称
            path: 要失效的目录路径
        """
        from app.core.database import get_session
        from sqlalchemy import text

        normalized_path = self._normalize_path(path)

        async with get_session() as session:
            result = await session.execute(
                text("""
                DELETE FROM path_id_cache
                WHERE library_name = :library_name AND path = :path
                """),
                {"library_name": library_name, "path": normalized_path},
            )
            await session.commit()
            count = result.rowcount or 0
        logger.debug(f"缓存失效: {library_name}:{normalized_path} (删除 {count} 条)")

    async def find_nearest_cached_ancestor(
        self, library_name: str, path: str
    ) -> tuple[str | None, str]:
        """
        查找最近的已缓存祖先目录。

        从完整路径开始，逐级向上查找已缓存的路径，返回最近的缓存 ID 和剩余路径。

        Args:
            library_name: 媒体库名称
            path: 目标路径，如 /云下载/测试/目标/其他/MUDR-359

        Returns:
            tuple: (缓存的路径ID字符串, 需要继续遍历的相对路径)
            如 /云下载/测试/目标 已缓存，则返回 ("cid", "其他/MUDR-359")
            若无任何缓存，返回 ("0", "云下载/测试/目标/其他/MUDR-359")
        """
        parts = path.strip("/").split("/")

        for i in range(len(parts), 0, -1):
            ancestor_path = "/" + "/".join(parts[:i])
            cached_id = await self.get_cached_path_id(library_name, ancestor_path)
            if cached_id is not None:
                remaining_path = "/".join(parts[i:]) if i < len(parts) else ""
                logger.debug(
                    f"找到缓存祖先: {ancestor_path} -> {cached_id}, 剩余路径: {remaining_path or '(空)'}"
                )
                return str(cached_id), remaining_path

        logger.debug("未找到任何缓存祖先，从根目录开始遍历")
        return "0", path.strip("/")

    async def cleanup_expired_cache(self, batch_size: int = 1000) -> int:
        """
        清理过期缓存记录（批量删除）。

        Args:
            batch_size: 单次清理最大数量，默认 1000

        Returns:
            int: 实际删除的记录数
        """
        from app.core.database import get_session
        from sqlalchemy import text

        now = int(time.time())

        async with get_session() as session:
            result = await session.execute(
                text("""
                DELETE FROM path_id_cache
                WHERE id IN (
                    SELECT id FROM path_id_cache
                    WHERE expires_at <= :now
                    LIMIT :limit
                )
                """),
                {"now": now, "limit": batch_size},
            )
            await session.commit()
            total_deleted = result.rowcount or 0

        if total_deleted > 0:
            logger.info(f"清理过期缓存: 删除 {total_deleted} 条记录")
        return total_deleted
