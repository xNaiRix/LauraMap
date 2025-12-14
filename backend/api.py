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

@app.get("/temporary_for_db")
async def changeDB():
    # for point in d:
    #     f = await update_item(table_name="Points", **point)
    #     print(f)
    # d = []
    print(x:= await get_items(table_name="Points"))
    # print(d)
    #print(await update_item(table_name="Points", id=10, avatar_id=17))
    # for i in range(60):
    #     print(await get_item(table_name="Media", id=i))

    return {"status":"offed", "points":x}
