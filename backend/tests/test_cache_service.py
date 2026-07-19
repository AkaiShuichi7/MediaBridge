"""
@description 路径 ID 缓存服务测试
@responsibility 验证 PathIdCacheService 的路径规范化、缓存读写和清理功能
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.cache.path_cache import PathIdCacheService


class TestPathNormalization:
    """测试路径规范化方法"""

    def setup_method(self):
        self.service = PathIdCacheService()

    def test_normalize_simple_path(self):
        """测试简单路径规范化"""
        assert self.service._normalize_path("/云下载/电影") == "/云下载/电影"

    def test_normalize_trailing_slash(self):
        """测试去除末尾斜杠"""
        assert self.service._normalize_path("/云下载/电影/") == "/云下载/电影"

    def test_normalize_no_leading_slash(self):
        """测试确保开头斜杠"""
        assert self.service._normalize_path("云下载/电影") == "/云下载/电影"

    def test_normalize_root(self):
        """测试根路径规范化"""
        assert self.service._normalize_path("/") == "/"

    def test_normalize_empty(self):
        """测试空路径规范化"""
        assert self.service._normalize_path("") == "/"

    def test_normalize_double_slashes(self):
        """测试去除多余斜杠"""
        assert self.service._normalize_path("//云下载//电影//") == "/云下载/电影"


class TestTempDirectoryDetection:
    """测试临时目录检测（番号目录识别）"""

    def setup_method(self):
        self.service = PathIdCacheService()

    def test_detect_typical_fanhao(self):
        """测试检测典型番号目录"""
        assert self.service._is_temp_directory("/media/MUDR-359") is True
        assert self.service._is_temp_directory("/media/SSIS-001") is True
        assert self.service._is_temp_directory("/media/ABP-123") is True

    def test_not_temp_regular_dir(self):
        """测试普通目录不是临时目录"""
        assert self.service._is_temp_directory("/云下载/电影") is False
        assert self.service._is_temp_directory("/媒体库") is False

    def test_not_temp_lowercase(self):
        """测试小写字母不匹配番号模式"""
        assert self.service._is_temp_directory("/media/mudr-359") is False

    def test_not_temp_no_digits(self):
        """测试无数字不匹配"""
        assert self.service._is_temp_directory("/media/MUDR") is False


class TestGetCachedPathId:
    """测试缓存读取功能"""

    def setup_method(self):
        self.service = PathIdCacheService()

    def _make_mock_ctx(self, scalar_value):
        """构造 mock DB session 上下文"""
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = scalar_value
        mock_session.execute = AsyncMock(return_value=mock_result)

        mock_ctx = MagicMock()
        mock_ctx.__aenter__ = AsyncMock(return_value=mock_session)
        mock_ctx.__aexit__ = AsyncMock(return_value=None)
        return mock_ctx

    @pytest.mark.asyncio
    async def test_cache_hit(self):
        """测试缓存命中返回正确 ID"""
        # get_session 在方法体内部导入，需要 patch app.core.database.get_session
        with patch(
            "app.core.database.get_session", return_value=self._make_mock_ctx(12345)
        ):
            result = await self.service.get_cached_path_id("电影库", "/云下载/电影")
            assert result == 12345

    @pytest.mark.asyncio
    async def test_cache_miss(self):
        """测试缓存未命中返回 None"""
        with patch(
            "app.core.database.get_session", return_value=self._make_mock_ctx(None)
        ):
            result = await self.service.get_cached_path_id("电影库", "/不存在的路径")
            assert result is None

    @pytest.mark.asyncio
    async def test_path_normalized_before_query(self):
        """测试查询前路径已规范化（带尾斜杠与不带结果相同）"""
        with patch(
            "app.core.database.get_session", return_value=self._make_mock_ctx(99)
        ):
            result = await self.service.get_cached_path_id("电影库", "/云下载/电影/")
            assert result == 99


class TestSetCachedPathId:
    """测试缓存写入功能"""

    def setup_method(self):
        self.service = PathIdCacheService()

    def _make_mock_ctx(self):
        """构造 mock DB session 上下文（写操作）"""
        mock_session = AsyncMock()
        mock_session.execute = AsyncMock()
        mock_session.commit = AsyncMock()

        mock_ctx = MagicMock()
        mock_ctx.__aenter__ = AsyncMock(return_value=mock_session)
        mock_ctx.__aexit__ = AsyncMock(return_value=None)
        return mock_ctx, mock_session

    @pytest.mark.asyncio
    async def test_set_cache_calls_upsert(self):
        """测试写缓存调用 UPSERT SQL"""
        mock_ctx, mock_session = self._make_mock_ctx()
        with patch("app.core.database.get_session", return_value=mock_ctx):
            await self.service.set_cached_path_id("电影库", "/云下载/电影", 67890)

        mock_session.execute.assert_called_once()
        mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_set_cache_with_custom_ttl(self):
        """测试自定义 TTL 写入缓存"""
        mock_ctx, mock_session = self._make_mock_ctx()
        with patch("app.core.database.get_session", return_value=mock_ctx):
            await self.service.set_cached_path_id(
                "电影库", "/路径", 100, ttl_seconds=30
            )

        mock_session.commit.assert_called_once()


class TestInvalidateCache:
    """测试缓存失效功能"""

    def setup_method(self):
        self.service = PathIdCacheService()

    @pytest.mark.asyncio
    async def test_invalidate_calls_delete(self):
        """测试缓存失效调用 DELETE SQL"""
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.rowcount = 1
        mock_session.execute = AsyncMock(return_value=mock_result)
        mock_session.commit = AsyncMock()

        mock_ctx = MagicMock()
        mock_ctx.__aenter__ = AsyncMock(return_value=mock_session)
        mock_ctx.__aexit__ = AsyncMock(return_value=None)

        with patch("app.core.database.get_session", return_value=mock_ctx):
            await self.service.invalidate_cache("电影库", "/云下载/旧路径")

        mock_session.execute.assert_called_once()
        mock_session.commit.assert_called_once()


class TestCleanupExpiredCache:
    """测试过期缓存清理功能"""

    def setup_method(self):
        self.service = PathIdCacheService()

    def _make_mock_ctx(self, rowcount):
        """构造带 rowcount 的 mock session"""
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.rowcount = rowcount
        mock_session.execute = AsyncMock(return_value=mock_result)
        mock_session.commit = AsyncMock()

        mock_ctx = MagicMock()
        mock_ctx.__aenter__ = AsyncMock(return_value=mock_session)
        mock_ctx.__aexit__ = AsyncMock(return_value=None)
        return mock_ctx

    @pytest.mark.asyncio
    async def test_cleanup_returns_deleted_count(self):
        """测试清理返回实际删除数量"""
        with patch(
            "app.core.database.get_session", return_value=self._make_mock_ctx(5)
        ):
            count = await self.service.cleanup_expired_cache()
        assert count == 5

    @pytest.mark.asyncio
    async def test_cleanup_returns_zero_when_none_expired(self):
        """测试无过期记录时返回 0"""
        with patch(
            "app.core.database.get_session", return_value=self._make_mock_ctx(0)
        ):
            count = await self.service.cleanup_expired_cache()
        assert count == 0

    @pytest.mark.asyncio
    async def test_cleanup_custom_batch_size(self):
        """测试自定义批次大小"""
        with patch(
            "app.core.database.get_session", return_value=self._make_mock_ctx(3)
        ):
            count = await self.service.cleanup_expired_cache(batch_size=50)
        assert count == 3
