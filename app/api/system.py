"""
@description 系统状态接口
@responsibility 处理系统状态和监控任务状态的查询
"""

from typing import TYPE_CHECKING, Optional
from datetime import datetime

from fastapi import APIRouter, Depends

from app.schemas.api import StatusResponse, success_response, ApiResponse
from app.core.dependencies import get_task_monitor, get_p115_client

if TYPE_CHECKING:
    from app.tasks.monitor import TaskMonitor
    from app.services.p115_client import P115Client

router = APIRouter()

# 最近检查时间（模块级状态，供 monitor.py 调用 update_last_check_time 更新）
_last_check_time: Optional[datetime] = None


def update_last_check_time():
    """
    更新最近检查时间。

    由 TaskMonitor 在每次轮询后调用，用于在系统状态接口中展示。
    """
    global _last_check_time
    _last_check_time = datetime.now()


@router.get("/status", response_model=ApiResponse[StatusResponse])
async def get_status(
    task_monitor: "TaskMonitor" = Depends(get_task_monitor),
    p115_client: "P115Client" = Depends(get_p115_client),
):
    """获取系统运行状态，包括监控任务状态和活跃离线任务数量。"""
    monitor_running = False
    if task_monitor is not None:
        if hasattr(task_monitor, "_task") and task_monitor._task is not None:
            monitor_running = not task_monitor._task.done()
        elif hasattr(task_monitor, "_stop_event"):
            monitor_running = not task_monitor._stop_event.is_set()

    active_tasks = 0
    if p115_client is not None:
        try:
            result = await p115_client.get_offline_tasks()
            if result.get("state"):
                tasks = result.get("tasks", [])
                active_tasks = sum(1 for t in tasks if t.get("status") == 0)
        except Exception:
            pass

    return success_response(
        data=StatusResponse(
            monitor_running=monitor_running,
            active_tasks=active_tasks,
            last_check_time=_last_check_time.isoformat() if _last_check_time else None,
        ),
        message="获取系统状态成功",
    )
