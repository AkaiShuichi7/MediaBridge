from pydantic import BaseModel

class OpenListItem(BaseModel):
    id: int
    name: str
    # ... 其他 OpenList 相关的字段
