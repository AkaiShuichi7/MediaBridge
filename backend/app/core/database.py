"""
@description 异步数据库连接管理
@responsibility 提供 SQLAlchemy 异步引擎、会话管理和数据库初始化
"""

import os
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DEFAULT_DATABASE_URL = "sqlite+aiosqlite:///./db/data.db"

engine = None
async_session_local = None
Base = declarative_base()


def init_engine(database_url: str | None = None):
    """初始化数据库引擎和会话工厂，仅在配置确定后调用一次。"""
    global engine, async_session_local

    url = database_url or DEFAULT_DATABASE_URL
    engine = create_async_engine(
        url,
        echo=False,
        connect_args={"check_same_thread": False},
    )
    async_session_local = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


def get_database_url() -> str:
    """获取数据库 URL，优先级：环境变量 > 传入参数 > 默认值。"""
    return os.environ.get("DATABASE_URL", DEFAULT_DATABASE_URL)


async def init_db(database_url: str | None = None):
    """初始化数据库引擎并创建所有表。"""
    from app.models.offline_task import OfflineTask
    from app.models.organize_record import OrganizeRecord
    from app.models.path_id_cache import PathIdCache

    url = database_url or get_database_url()
    init_engine(url)

    # SQLite 相对路径 → 确保目录存在
    if url.startswith("sqlite"):
        db_path = url.split("///")[-1]
        if db_path.startswith("./"):
            db_path = db_path[2:]
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def get_session():
    """异步会话上下文管理器。"""
    async with async_session_local() as session:
        try:
            yield session
        finally:
            await session.close()
