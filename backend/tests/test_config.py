"""
@description 配置管理模块测试
@responsibility 验证配置加载、验证、环境变量覆盖功能
"""

import os
import tempfile
from errno import EBUSY
from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from app.core.config import Config, load_config, save_config


# 测试用的合法 YAML 配置内容
SAMPLE_CONFIG_YAML = """
cloud:
  poll_interval_min: 30
  poll_interval_max: 60
  p115:
    cookies: "UID=test_uid; CID=test_cid; SEID=test_seid"
media:
  min_transfer_size: 200
  libraries:
    - name: "测试库"
      download_path: "/downloads"
      target_path: "/target"
      type: "system"
  video_formats:
    - "mp4"
    - "mkv"
  xx:
    remove_keywords: ["关键词1", "关键词2"]
"""


class TestLoadConfigSuccess:
    """测试配置文件加载成功场景"""

    def test_load_config_success(self, tmp_path, monkeypatch):
        """验证配置文件加载成功"""
        # 创建临时配置文件并注入 CONFIG_PATH
        config_file = tmp_path / "config.yaml"
        config_file.write_text(SAMPLE_CONFIG_YAML, encoding="utf-8")
        monkeypatch.setenv("CONFIG_PATH", str(config_file))

        config = load_config()

        # 验证加载成功
        assert isinstance(config, Config)
        assert config.cloud is not None
        assert config.media is not None

        # 验证 cloud 配置
        assert config.cloud.p115.cookies is not None
        assert config.cloud.poll_interval_min > 0
        assert config.cloud.poll_interval_max > 0

        # 验证 media 配置
        assert config.media.min_transfer_size > 0
        assert len(config.media.libraries) > 0
        assert len(config.media.video_formats) > 0

        # 验证第一个 library 配置
        lib = config.media.libraries[0]
        assert lib.name is not None
        assert lib.download_path is not None
        assert lib.target_path is not None
        assert lib.type is not None


class TestSaveConfig:
    def test_save_config_falls_back_for_busy_bind_mount(self, tmp_path, monkeypatch):
        config_file = tmp_path / "config.yaml"
        config_file.write_text(SAMPLE_CONFIG_YAML, encoding="utf-8")
        monkeypatch.setenv("CONFIG_PATH", str(config_file))
        config = load_config()
        config.media.video_formats.append("webm")

        def raise_busy_replace(self, target):
            raise OSError(EBUSY, "Device or resource busy")

        monkeypatch.setattr(Path, "replace", raise_busy_replace)
        save_config(config)

        persisted = yaml.safe_load(config_file.read_text(encoding="utf-8"))
        assert "webm" in persisted["media"]["video_formats"]


class TestConfigNotExistsGenerateTemplate:
    """测试配置不存在时生成模板"""

    def test_config_not_exists_generate_template(self):
        """验证配置文件不存在时生成模板并抛出 SystemExit"""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.yaml"
            template_path = Path(tmpdir) / "config.example.yaml"

            # 临时修改环境变量指向临时目录
            old_config_path = os.environ.get("CONFIG_PATH")
            try:
                os.environ["CONFIG_PATH"] = str(config_path)

                # 验证配置文件不存在时抛出 SystemExit
                with pytest.raises(SystemExit):
                    load_config()

                # 验证生成了模板文件
                assert template_path.exists(), "应生成 config.example.yaml"

                # 验证模板文件有效
                with open(template_path, encoding="utf-8") as f:
                    content = yaml.safe_load(f)
                    assert "cloud" in content
                    assert "media" in content
            finally:
                if old_config_path:
                    os.environ["CONFIG_PATH"] = old_config_path
                elif "CONFIG_PATH" in os.environ:
                    del os.environ["CONFIG_PATH"]


class TestEnvOverrideCookies:
    """测试环境变量覆盖 cookies"""

    def test_env_override_cookies(self, tmp_path, monkeypatch):
        """验证 P115_COOKIES 环境变量覆盖配置中的 cookies"""
        # 创建临时配置文件
        config_file = tmp_path / "config.yaml"
        config_file.write_text(SAMPLE_CONFIG_YAML, encoding="utf-8")
        monkeypatch.setenv("CONFIG_PATH", str(config_file))

        test_cookies = "UID=test_uid; CID=test_cid; SEID=test_seid; KID=test_kid"
        monkeypatch.setenv("P115_COOKIES", test_cookies)

        config = load_config()

        # 验证环境变量覆盖了配置文件中的 cookies
        assert config.cloud.p115.cookies == test_cookies


class TestInvalidConfigValidation:
    """测试无效配置验证"""

    def test_invalid_config_validation(self):
        """验证无效配置触发 Pydantic ValidationError"""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.yaml"

            # 创建无效配置（缺少必要字段）
            invalid_config = {
                "cloud": {
                    # 缺少 p115 子块（cookies）以及云盘公共字段（poll_interval_min、poll_interval_max）
                },
                "media": {
                    # 缺少 libraries、video_formats
                },
            }

            with open(config_path, "w", encoding="utf-8") as f:
                yaml.dump(invalid_config, f)

            old_config_path = os.environ.get("CONFIG_PATH")
            try:
                os.environ["CONFIG_PATH"] = str(config_path)

                # 验证无效配置抛出 ValidationError
                with pytest.raises(ValidationError):
                    load_config()
            finally:
                if old_config_path:
                    os.environ["CONFIG_PATH"] = old_config_path
                elif "CONFIG_PATH" in os.environ:
                    del os.environ["CONFIG_PATH"]


class TestLibraryConfigValidation:
    """测试媒体库配置验证"""

    def test_library_config_structure(self, tmp_path, monkeypatch):
        """验证媒体库配置结构"""
        config_file = tmp_path / "config.yaml"
        config_file.write_text(SAMPLE_CONFIG_YAML, encoding="utf-8")
        monkeypatch.setenv("CONFIG_PATH", str(config_file))

        config = load_config()

        # 验证 libraries 结构
        for lib in config.media.libraries:
            assert hasattr(lib, "name")
            assert hasattr(lib, "download_path")
            assert hasattr(lib, "target_path")
            assert hasattr(lib, "type")
            assert hasattr(lib, "min_transfer_size")


class TestXXConfigValidation:
    """测试 xx 配置验证"""

    def test_xx_config_structure(self, tmp_path, monkeypatch):
        """验证 xx（成人片库）配置结构"""
        config_file = tmp_path / "config.yaml"
        config_file.write_text(SAMPLE_CONFIG_YAML, encoding="utf-8")
        monkeypatch.setenv("CONFIG_PATH", str(config_file))

        config = load_config()

        # 验证 xx 配置
        assert config.media.xx is not None
        assert hasattr(config.media.xx, "remove_keywords")
        assert isinstance(config.media.xx.remove_keywords, list)
        assert len(config.media.xx.remove_keywords) > 0
