from fastapi import FastAPI
from fastapi import Depends, Query, Path, HTTPException, status, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from fastapi import Depends, Query, Path, HTTPException, status, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from datetime import date
from dateutil.relativedelta import relativedelta
import os
from dotenv import load_dotenv

import map_handler
from models import MapResponse, MapPointPreview

app = FastAPI(title="LauraMap API", version="1.0.0")

os.makedirs("uploads/map_items", exist_ok=True)
os.makedirs("uploads/animals", exist_ok=True)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
load_dotenv()
API_PORT = int(os.getenv("API_PORT", "8000"))
BACKEND_IP = os.getenv("BACKEND_IP", "0.0.0.0")
HOST = "http://" + BACKEND_IP + ":" + str(API_PORT)
map_handler.init()
my_map= map_handler.my_map


@app.get("/")
async def root():
    return {"message": "LauraMap API is running", "version": "1.0.0", "docs": "/docs", "redoc": "/redoc"}
@app.get("/favicon.ico")
async def favicon_ico():
    return None
@app.options("/{path:path}")
async def options_handler(path: str):
    return {"message": "OK"}


@app.get("/api/map", response_model=MapResponse)
async def getMap()->MapResponse:
    return await my_map.brief()



#получить краткую информацию о точке
@app.get("/api/map/points/{id}/preview")
async def getPointPreview(id:int)->MapPointPreview:
    return await my_map.point_preview(id=id)

#полная информация о точке
@app.get("/api/map/points/{id}")
async def getPoint(id:int):
    pass

#список всех животных с краткой инфой по каждому
@app.get("/api/map/animals")
async def getAnimals():
    return ["apple", "cat", "спасите"]


#========================================================= TEMPORARY ONLY FOR ADDING/UPDATING WHILE WHERE IS NO API FOR CHANGING DATABASE

from database import get_item, insert_item, update_item, get_items
#нужны только для первоначального добавления точек (лень было выносить в отдельный файл и его потом парсить xd)
points = [{'x': 850, 'y': 1820, 'name': 'Кубанский волк'},
          {'x': 1587, 'y': 1820, 'name': 'Пятнистый олень'},
          {'x': 2240, 'y': 1820, 'name': 'Серна'},
          {'x': 738, 'y': 496, 'name': 'Кабан'},
          {'x': 1168, 'y': 496, 'name': 'Бурый медведь'},
          {'x': 1785, 'y': 526, 'name': 'Шакал'},
          {'x': 2410, 'y': 585, 'name': 'Леопард', "size":168},
          {'x': 3069, 'y': 585, 'name': 'Рысь', "size":168},
          {'x': 3069, 'y': 198, 'name': 'Лиса 1', "size":168},
          {'x': 2993, 'y': 1820, 'name': 'Кавказская косуля'},
          {'x': 3359, 'y': 1820, 'name': 'Тур'},
          {'x': 4292, 'y': 1820, 'name': 'Кавказские олени 1'},
          {'x': 4672, 'y': 1820, 'name': 'Кавказские олени 2'},
          {'x': 5216, 'y': 955, 'name': 'Орёл'},
          {'x': 4607, 'y': 289, 'name': 'Лебедь'},
          {'x': 4904, 'y': 289, 'name': 'Гусь'},
          {'x': 5201, 'y': 289, 'name': 'Кряква'},
          {'x':5498, 'y':289, 'name':'Утка-мандаринка'},#готово
          {'x': 6206, 'y': 1593, 'name': 'Горный зубр'},
          {'x': 6656, 'y': 1288, 'name': 'Зубры 2'},
          {'x': 6603, 'y': 774, 'name': 'Зубры 3'},
          {'x': 5758, 'y': 1000, 'name': 'Стервятник', "size":100},
          {'x': 4597, 'y': 943, 'name': 'Коршун', 'size':100},
          {'x': 4730, 'y': 968, 'name': 'Ястреб', 'size':100},
          {'x': 4042, 'y': 883, 'name': 'Енот-полоскун',"size":100},
          {'x': 4201, 'y': 883, 'name': 'Барсук', 'size':100},
          {'x': 4201, 'y': 615, 'name': 'Лесной кот', 'size':100},
          {'x':3984, 'y':668, 'name':"Енотовидная собака", 'size':100},
          {'x':4073, 'y':579, 'name':"Лиса 2", 'size':100}]#29 точек



@app.get("/temporary_for_db")
async def changeDB():
    # print(len(points))
    # for id in range(1, 30):
    #     print(await get_item(table_name="Points", id=id))
    # for point in points:
    #         d = point
    #         id = await insert_item(table_name="Points", **d)
    #         print(id)
    #         print("==========================")

    #Добавление животных
#     animal_id=10
#     avatar_url = "/uploads/animals/photo/18.png"
#     audio_url= "/uploads/animals/audio/51.mp3"
#     brief_info='''Косуля — небольшой олень, обитает в поймах рек и лесных полянах, иногда в горах. Самцы весят 22–32 кг, рога небольшие, изогнутые.
# Питаются растительностью, ягодами и грибами, зимой ветками и почками. Суточно съедают до 4 кг пищи и пьют около 1,5 л воды.'''
#     avatar_id = (await insert_item(table_name="Media", media_url=avatar_url, media_type='photo')).get("id", None)
#     audio_id = (await insert_item(table_name="Media", media_url=audio_url, media_type='audio')).get("id", None)
#     print(avatar_id, audio_id)
#     if not audio_id or not avatar_id:
#         print(avatar_id, audio_id)
#         return {"status":"error"}
#     s = await update_item(table_name="Points", id=animal_id, avatar_id=avatar_id, audio_id=audio_id, brief_info=brief_info)
#     print(s)
#     print(a:=(await get_item(table_name="Points", id=animal_id)))
#     print(b:=(await get_item(table_name="Media", id=audio_id)))
#     print(c:=(await get_item(table_name="Media", id=avatar_id)))
#     return {"status": "success",
#             "animal": a,
#             "audio":b,
#             "avatar":c}

    # for id in range(1,31):
    #     m = await get_item(table_name="Points", id=id)
    #     print(m)


    # d = []
    for i in range(1, 32):
        print(await get_item(table_name="Points", id=i))
    return {"status":"offed", "points":None}
