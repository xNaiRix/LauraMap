from pydantic import BaseModel, HttpUrl
from typing import List,Dict, Optional, Literal
from datetime import datetime

class MapPointBrief(BaseModel):
    id:int
    x:int
    y:int
    name:str
    avatar_url:Optional[str]
    size:int

class MapPointMedium(BaseModel):
    id:int
    name:str
    photo_url:Optional[str]
    audio_url:Optional[str]
    brief_info:str="fish fish fish"

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


class Point:
    def __init__(self, id:int, name:str, avatar_url:str, place:tuple[int,int], size:int,article_id:int, audio_url:str="", info:str=""):
        self.id=id
        self.name=name
        self.avatar_url=avatar_url
        self.place=place
        self.info=info
        self.size=size
        self.audio_url = audio_url
        self.article_id = article_id
    def brief(self):
        return MapPointBrief(id=self.id, x=self.place[0], y = self.place[1], name=self.name, avatar_url=self.avatar_url, size=self.size)
    def medium(self):
        return MapPointBrief(id=self.id, x=self.place[0], y = self.place[1], name=self.name, avatar_url=self.avatar_url,size=self.size)

