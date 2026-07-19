"""
@description 云盘文件类型定义
@responsibility 定义 CloudFile 数据类和 115 云盘字段映射，提供字段规范化基础类型
"""

from dataclasses import dataclass, field

# 115 原始字段名 → 标准字段名映射表
P115_FIELD_MAP: dict = {
    "fid": "file_id",  # 文件唯一 ID
    "n": "name",  # 文件/目录名称
    "s": "size",  # 文件大小（字节）
    "cid": "parent_id",  # 父目录 ID
    "pid": "pick_code",  # 提取码
}


@dataclass
class CloudFile:
    """云盘文件/目录的标准化数据类"""

    file_id: str  # 文件唯一标识
    name: str  # 文件或目录名称
    size: int  # 文件大小（字节），目录为 0
    parent_id: str  # 父目录 ID
    is_directory: bool  # 是否为目录（True=目录，False=文件）
    pick_code: str = ""  # 提取码，目录可能为空

    @classmethod
    def from_p115_dict(cls, raw: dict) -> "CloudFile":
        """
        将 115 原始响应字典转换为标准 CloudFile 对象

        Args:
            raw: 115 API 返回的原始字典，字段为短名如 fid、n、s、cid、pid

        Returns:
            标准化的 CloudFile 实例

        Note:
            通过是否含有 `fid` 字段区分文件与目录：
            - 有 `fid` → 文件（is_directory=False）
            - 无 `fid` → 目录（is_directory=True）
        """
        # fid 存在为文件，缺失为目录
        is_directory = "fid" not in raw

        return cls(
            file_id=str(raw.get("fid", raw.get("cid", ""))),
            name=raw.get("n", ""),
            size=int(raw.get("s", 0)),
            parent_id=str(raw.get("cid", "")),
            is_directory=is_directory,
            pick_code=raw.get("pid", ""),
        )
