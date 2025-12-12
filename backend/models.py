from pydantic import BaseModel, Field
from typing import List,Dict, Optional, Literal
from datetime import datetime
from database import get_item, get_items

class MapPointBrief(BaseModel):
    id:int
    x:int#координаты
    y:int
    name:str
    avatar_url:Optional[str]
    size:int =  Field(default=255, ge=1)
    status:Literal["success", "error"]
    @classmethod
    async def create(cls, **point_data):
        avatar_url = None
        if point_data.get('avatar_id'):
            media = await get_item(table_name="Media", id=point_data['avatar_id'])
            avatar_url = media.get("media_url") if media else None
        
        return cls(
            status="success",
            id=point_data['id'],
            x=point_data['x'],
            y=point_data['y'],
            name=point_data['name'],
            avatar_url=avatar_url,
            size=point_data.get('size', 255),
        )


class MapPointPreview(BaseModel):
    id:int
    name:str
    avatar_url:Optional[str]
    audio_url:Optional[str]
    brief_info:Optional[str]
    size:int =  Field(default=255, ge=1)
    status:Literal["success", "error"]

    @classmethod
    async def create(cls, **point_data):
        avatar_url = None
        if point_data.get('avatar_id'):
            media = await get_item(table_name="Media", id=point_data['avatar_id'])
            avatar_url = media.get("media_url") if media else None
        audio_url = None
        if point_data.get('audio_id'):
            media = await get_item(table_name="Media", id=point_data['audio_id'])
            audio_url = media.get("media_url") if media else None

        return cls(
            status="success",
            id=point_data['id'],
            name=point_data['name'],
            avatar_url=avatar_url,
            audio_url=audio_url,
            brief_info=point_data["brief_info"],
            size=point_data.get('size', 255),
        )

class MapResponse(BaseModel):
    map_url:str
    tittle:str
    points:List[MapPointBrief]

class ArticleResponse(BaseModel):
    id: int
    title: str
    content_html: str
    created_at: datetime

#для БД таблиц
class PointCreate(BaseModel):
    name: str
    avatar_url: str
    x: int
    y: int
    size: int
    article_id: int

class PointDB(BaseModel):
    id: int
    name: str
    avatar_url: str
    x: int
    y: int
    size: int
    article_id: int
    created_at: datetime = None

class MediaCreate(BaseModel):
    point_id: int
    media_url: str
    url_type: Literal["photo", "video", "audio"]

class MediaDB(BaseModel):
    id: int
    point_id: int
    media_url: str
    url_type: str
    created_at: datetime = None

class ArticleCreate(BaseModel):
    title: str
    content_html: str

class ArticleDB(BaseModel):
    id: int
    title: str
    content_html: str
    created_at: datetime = None


