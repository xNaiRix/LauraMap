from models import MapPointBrief, MapResponse
from database import getItem
class Map:
    def __init__(self):
        self.map_image_path = "/uploads/map.svg"
        self.tittle="Карта Лауры"
        self.points_cnt = 26

    def brief(self):
        brief = MapResponse(map_url=self.map_image_path, tittle=self.tittle,points=list())
        for i in range(self.points_cnt):
            brief.points.append(getItem(tableName="Points", id=i).brief())
        return brief


my_map = None
def init():
    global my_map#ещё сделать подгрузку с бд?
    if not my_map:
        my_map = Map()