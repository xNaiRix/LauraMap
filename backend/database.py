##ОДНА БОЛЬШАЯ ЗАГЛУШКА

from models import Point
from typing import List

import aiosqlite
import asyncio
import os
from dotenv import load_dotenv
from typing import List, Optional, Dict
from pathlib import Path

pre_points = [{"name":"Кубанский волк", "place":(37, 722)}, 
                    {"name":"Пятнистый олень", "place": (37, 1459)},
                    {"name": "Серны", "place":(37,2112)},
                    {"name":"Кабан", "place":(1361, 610)},
                    {"name":"Бурый медведь", "place": (1361, 1040)},
                    {"name": "Шакалы", "place":(1331, 1657)},
                    {"name":"Леопарды","place":(1309, 2305),"size":168},
                    {"name":"Рыси", "place":(1306,2972), "size":168},
                    {"name":"Лисы", "place":(1703,2985), "size":168},
                    {"name":"Кавказские косули", "place":(37, 2865)},
                    {"name":"Западнокавказские туры", "place":(37, 3231)},
                    {"name":"Кавказские олени", "place":(37, 4164)},
                    {"name":"Кавказские олени", "place":(37, 4544)},
                    {"name":"Орлы", "place":(902, 5088)},
                    {"name":"Гуси", "place":(1568,4512)},
                    {"name":"Утки", "place":(1568,4911)},
                    {"name":"Кряквы", "place":(1568,5310)},
                    {"name":"Зубры", "place":(264, 6078)},
                    {"name":"Зубры", "place":(569, 6528)},
                    {"name":"Зубры", "place":(1083, 6475)},
                    {"name":"Стервятники", "place":(935,5708), "size":100},
                    {"name":"Коршуны", "place":(992,4547), "size":100},
                    {"name":"Ястребы", "place":(967, 4680), "size":100},
                    {"name":"Еноты", "place":(1052, 3992), "size":100},
                    {"name":"Барсук","place":(1052, 4151), "size":100},
                    {"name":"Кошки", "place":(1320, 4151), "size":100}]



database = []
for i, point in enumerate(pre_points):
    database.append(dict(id=i, name=point["name"], place=point["place"], avatar_url=f"/uploads/map_items/{i}.png", info="", size=point.get("size", 255),article_id=i))
database_init=False
async def get_db_path():
    global database_init
    database_init = True
    BASE_DIR = Path(__file__).parent
    database_path = os.getenv("DATABASE_URL", str(BASE_DIR / "database.db"))
    return database_path
async def init():
    database_path = await get_db_path()
    async with aiosqlite.connect(database_path) as db:
        await db.execute('''
        CREATE TABLE IF NOT EXISTS Articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article_html TEXT
        )
    ''')
        await db.commit()

        await db.execute('''
        CREATE TABLE IF NOT EXISTS Points (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            avatar_url TEXT,
            x INTEGER,
            y INTEGER,
            size INTEGER,
            brief_info TEXT,
            article_id INTEGER,
            FOREIGN KEY (article_id) REFERENCES Articles(id) ON DELETE SET NULL
        )
    ''')
        await db.commit()

        await db.execute('''
        CREATE TABLE IF NOT EXISTS Media (
            point_id INTEGER,
            media_url TEXT,
            url_type TEXT NOT NULL CHECK (url_type IN ('photo', 'video', 'audio')),
            
            PRIMARY KEY (point_id, media_url)
            FOREIGN KEY (point_id) REFERENCES points(id) ON DELETE CASCADE
        )
    ''')
        await db.commit()


#==========================================


def get_item(tableName:str, id:int)->Point|None:
    for point in database:
        if point["id"] == id:
            return point
    return None

async def getItems(tableName:str, id:List[int]):
    pass

async def updateItem(tableName:str, id:int, **kwargs)->bool:#если нет, то добавляет такой элемент. Если нет атрибута, то не трогает этот атрибут
    pass
async def deleteItem(tableName:str, id:int)->bool:
    pass
