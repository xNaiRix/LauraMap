from models import MapPointBrief, MapResponse, Point
from database import get_item, insert_item

#нужны только для первоначального добавления точек (лень было выносить в отдельный файл и его потом парсить xd)
points = [{'x': 850, 'y': 1820, 'name': 'Кубанский волк'},
          {'x': 1587, 'y': 1820, 'name': 'Пятнистый олень'},
          {'x': 2240, 'y': 1820, 'name': 'Серна'},
          {'x': 738, 'y': 496, 'name': 'Кабан'},
          {'x': 1168, 'y': 496, 'name': 'Бурый медведь'},
          {'x': 1785, 'y': 526, 'name': 'Шакал'},
          {'x': 2410, 'y': 585, 'name': 'Леопард'},
          {'x': 3069, 'y': 585, 'name': 'Рысь'},
          {'x': 3069, 'y': 198, 'name': 'Лиса'},
          {'x': 2993, 'y': 1820, 'name': 'Кавказская косуля'},
          {'x': 3359, 'y': 1820, 'name': 'Тур'},
          {'x': 4292, 'y': 1820, 'name': 'Кавказские олени 1'},
          {'x': 4672, 'y': 1820, 'name': 'Кавказские олени 2'},
          {'x': 5216, 'y': 955, 'name': 'Орёл'},
          {'x': 4640, 'y': 289, 'name': 'Лебедь'},
          {'x': 5039, 'y': 289, 'name': 'Водоплавающие птицы 2'},
          {'x': 5438, 'y': 289, 'name': 'Водоплавающие птицы 3'},
          {'x': 6206, 'y': 1593, 'name': 'Горный зубр'},
          {'x': 6656, 'y': 1288, 'name': 'Зубры 2'},
          {'x': 6603, 'y': 774, 'name': 'Зубры 3'},
          {'x': 5758, 'y': 1000, 'name': 'Стервятник'},
          {'x': 4597, 'y': 943, 'name': 'Коршун'},
          {'x': 4730, 'y': 968, 'name': 'Ястреб'},
          {'x': 4042, 'y': 883, 'name': 'Енот-полоскун'},
          {'x': 4201, 'y': 883, 'name': 'Барсук'},
          {'x': 4201, 'y': 615, 'name': 'Лесной кот'}]#26 точек

class Map:
    def __init__(self):
        self.map_image_path = "/uploads/map.svg"
        self.tittle="Карта Лауры"
        self.points_cnt = 26

    async def brief(self):
        # for point in points:
        #     await insert_item(table_name="Points", **point)
        try:
            brief = MapResponse(map_url=self.map_image_path, tittle=self.tittle,points=list())
            for i in range(1, self.points_cnt + 1):
                print(i)
                tmp = await get_item(table_name="Points", id=i)
                print(tmp)
                brief.points.append(Point(**tmp).brief())
        except Exception as e:
            print(e)
            return brief

        return brief


my_map = None
def init():
    global my_map#ещё сделать подгрузку с бд?
    if not my_map:
        my_map = Map()