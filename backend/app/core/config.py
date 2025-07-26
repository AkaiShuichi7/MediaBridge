from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # OpenList API
    OPENLIST_API_URL: Optional[str] = None
    OPENLIST_API_KEY: Optional[str] = None

    # Emby API
    EMBY_API_URL: Optional[str] = None
    EMBY_API_KEY: Optional[str] = None

    # Download paths
    DOWNLOAD_PATH: str = "/downloads"
    COMPLETED_PATH: str = "/completed"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# 创建一个全局可用的 settings 实例
settings = Settings()
