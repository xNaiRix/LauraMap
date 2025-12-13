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



