from pydantic import BaseModel

class EmbyItem(BaseModel):
    id: str
    title: str
    # ... 其他 Emby 相关的字段
