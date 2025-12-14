from models import MapPointPreview, MapResponse, MapPointBrief
from database import get_item, get_items, insert_item

class Point:
    def __init__(self, id:int, name:str,size:int, avatar_id:int|None=None, article_id:int|None=None, place:tuple[int,int]=(0,0), audio_id:int|None="", brief_info:str|None="", **kwargs):
        if 'x' in kwargs and "y" in kwargs:
            place = (kwargs["x"],kwargs["y"])
        self.id=id
        self.name=name
        self.avatar_id=avatar_id
        self.place=place
        self.brief_info=brief_info
        self.size=size
        self.audio_id = audio_id
        self.article_id = article_id
    async def brief(self):
        return await MapPointBrief.create(id=self.id, x=self.place[0], y = self.place[1], name=self.name, avatar_id=self.avatar_id, size=self.size)
    
    async def preview(self):
        return await MapPointPreview.create(id=self.id, name=self.name, avatar_id=self.avatar_id, audio_id=self.audio_id, brief_info=self.brief_info, size=self.size)


class Map:
    def __init__(self):
        self.map_image_path = "/uploads/map.svg"
        self.tittle="Карта Лауры"

    async def brief(self)->MapResponse:
        try:
            brief = MapResponse(map_url=self.map_image_path, tittle=self.tittle,points=list())
            points = await get_items(table_name="Points")
            print(points)
            for point in points:
                brief.points.append(await Point(**point).brief())
        except Exception as e:
            print(e)
            return brief

        return brief
    
    async def point_preview(self, id:int)->MapPointPreview|dict:
        try:
            point = await get_item(table_name="Points", id=id)
            print(point)
            return await MapPointPreview.create(**point)
        except Exception as e:
            print(e)
            return {"status":"error"}


my_map = None
def init():
    global my_map#ещё сделать подгрузку с бд?
    if not my_map:
        my_map = Map()