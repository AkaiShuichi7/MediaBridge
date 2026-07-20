"""
@description 配置管理接口
@responsibility 处理配置的查询和修改操作
"""

from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends

from app.schemas.api import (
    ConfigResponse,
    P115ConfigResponse,
    MediaConfigResponse,
    LibraryItem,
    XXConfigResponse,
    UpdateConfigRequest,
    UpdateConfigResponse,
    LibrariesResponse,
    success_response,
)
from app.core.dependencies import get_config as _get_config_dep
from app.core.config import save_config

if TYPE_CHECKING:
    from app.core.config import Config

router = APIRouter()


@router.get("/config")
async def get_config(config: "Config" = Depends(_get_config_dep)):
    """获取当前系统配置。"""
    libraries = [
        LibraryItem(
            name=lib.name,
            download_path=lib.download_path,
            target_path=lib.target_path,
            type=lib.type,
            min_transfer_size=lib.min_transfer_size,
        )
        for lib in config.media.libraries
    ]

    xx_config = XXConfigResponse(
        remove_keywords=config.media.xx.remove_keywords if config.media.xx else []
    )

    return success_response(
        data=ConfigResponse(
            p115=P115ConfigResponse(
                poll_interval_min=config.cloud.poll_interval_min,
                poll_interval_max=config.cloud.poll_interval_max,
            ),
            media=MediaConfigResponse(
                min_transfer_size=config.media.min_transfer_size,
                video_formats=config.media.video_formats,
                libraries=libraries,
                xx=xx_config,
            ),
        ),
        message="获取配置成功",
    )


@router.put("/config")
async def update_config(
    request: UpdateConfigRequest,
    config: "Config" = Depends(_get_config_dep),
):
    """更新系统配置项。"""
    # Validate a complete copy before mutating the shared runtime configuration.
    # This prevents an invalid partial request from leaving the application in an
    # unusable state when saving the YAML file fails validation.
    updated_config = config.model_copy(deep=True)

    if request.p115:
        if request.p115.poll_interval_min is not None:
            updated_config.cloud.poll_interval_min = request.p115.poll_interval_min
        if request.p115.poll_interval_max is not None:
            updated_config.cloud.poll_interval_max = request.p115.poll_interval_max

    if request.media:
        if request.media.min_transfer_size is not None:
            updated_config.media.min_transfer_size = request.media.min_transfer_size
        if request.media.video_formats is not None:
            updated_config.media.video_formats = request.media.video_formats
        if request.media.libraries is not None:
            updated_config.media.libraries = request.media.libraries
        if request.media.xx is not None:
            updated_config.media.xx.remove_keywords = request.media.xx.remove_keywords

    validated_config = type(config).model_validate(updated_config.model_dump())
    save_config(validated_config)
    config.cloud = validated_config.cloud
    config.media = validated_config.media

    return success_response(
        data=UpdateConfigResponse(message="配置更新成功"),
        message="配置更新成功",
    )


@router.get("/libraries")
async def get_libraries(config: "Config" = Depends(_get_config_dep)):
    """获取所有媒体库配置列表。"""
    libraries = [
        LibraryItem(
            name=lib.name,
            download_path=lib.download_path,
            target_path=lib.target_path,
            type=lib.type,
            min_transfer_size=lib.min_transfer_size,
        )
        for lib in config.media.libraries
    ]

    return success_response(
        data=LibrariesResponse(libraries=libraries),
        message="获取媒体库列表成功",
    )
