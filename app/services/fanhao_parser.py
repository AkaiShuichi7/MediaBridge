"""
@description 番号解析服务核心逻辑
@responsibility 番号提取、文件名标准化、目标路径生成
"""

import re
from pathlib import Path


FANHAO_PATTERN = re.compile(r"(?<![A-Z0-9])(?:[A-Z]{2,10}|[A-Z]\d{1,2})-\d{3,5}(?!\d)")


def remove_keywords(filename: str, keywords: list[str]) -> str:
    """
    从文件名中批量移除指定关键词。

    Args:
        filename: 原始文件名
        keywords: 需要移除的关键词列表

    Returns:
        移除关键词后的文件名
    """
    result = filename
    for keyword in keywords:
        result = result.replace(keyword, "")
    return result


def normalize_filename(filename: str) -> str:
    """
    标准化文件名：将点号替换为横线并转换为大写，保留扩展名。

    Args:
        filename: 原始文件名

    Returns:
        标准化后的文件名
    """
    parts = filename.rsplit(".", 1)
    if len(parts) == 2:
        name, ext = parts
        normalized_name = name.replace(".", "-").upper()
        return f"{normalized_name}.{ext}"
    else:
        return filename.upper()


def extract_fanhao(filename: str) -> str | None:
    """
    从文件名中提取日系影视番号（如 MUDR-359）。

    Args:
        filename: 文件名字符串

    Returns:
        找到的番号字符串，未找到则返回 None
    """
    match = FANHAO_PATTERN.search(filename)
    if match:
        return match.group()
    return None


def normalize_cd_suffix(filename: str, file_count: int) -> str:
    """
    规范化文件的 CD 分片后缀（将 A/B/1/2/PART1 等格式统一为 CD1/CD2）。

    当文件集合只有一个文件时不做任何变换。

    Args:
        filename: 原始文件名
        file_count: 同一番号下的文件总数

    Returns:
        标准化 CD 后缀后的文件名
    """
    parts = filename.rsplit(".", 1)
    if len(parts) != 2:
        return filename

    name, ext = parts

    if file_count == 1:
        return filename

    if "-" not in name:
        return filename

    suffix = name.split("-")[-1]

    letter_order = {"A": 1, "B": 2, "C": 3, "D": 4, "U": 1}
    numeric_mapping = {"1": "CD1", "2": "CD2", "3": "CD3", "4": "CD4"}
    part_mapping = {"PART1": "CD1", "PART2": "CD2", "PART3": "CD3", "PART4": "CD4"}

    base_name = "-".join(name.split("-")[:-1])

    if suffix in letter_order:
        order_num = letter_order[suffix]
        if order_num <= file_count:
            return f"{base_name}-CD{order_num}.{ext}"
        else:
            return f"{base_name}-CD1.{ext}"
    elif suffix in numeric_mapping:
        return f"{base_name}-{numeric_mapping[suffix]}.{ext}"
    elif suffix in part_mapping:
        return f"{base_name}-{part_mapping[suffix]}.{ext}"

    return filename


def generate_target_path(filename: str, target_dir: str, producer: str) -> str:
    """
    根据文件名和片商信息生成目标存储路径。

    路径格式：{target_dir}/{producer}/{番号}/{filename}

    Args:
        filename: 文件名（应已标准化）
        target_dir: 目标根目录
        producer: 片商名称

    Returns:
        完整的目标文件路径字符串

    Raises:
        ValueError: 无法从文件名中提取番号时抛出
    """
    target_dir = target_dir.rstrip("/")

    fanhao = extract_fanhao(filename)
    if not fanhao:
        raise ValueError(f"无法从文件名中提取番号: {filename}")

    return f"{target_dir}/{producer}/{fanhao}/{filename}"


def extract_producer(library_type: str) -> str | None:
    """
    从媒体库类型字符串中提取片商名称。

    仅适用于 "xx-{片商}" 格式的库类型（如 "xx-ABC" 返回 "ABC"）。

    Args:
        library_type: 媒体库类型字符串

    Returns:
        片商名称，不符合格式则返回 None
    """
    if not library_type or not library_type.startswith("xx-"):
        return None

    parts = library_type.split("-", 1)
    if len(parts) != 2 or not parts[1]:
        return None

    return parts[1]
