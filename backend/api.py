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
from models import MapResponse

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
    return my_map.brief()



#получить краткую информацию о точке
@app.get("/api/map/points/{id}/preview")
async def getPointPreview(id:int):
    pass

#полная информация о точке
@app.get("/api/map/points/{id}")
async def getPoint(id:int):
    pass

#список всех животных с краткой инфой по каждому
@app.get("/api/map/animals")
async def getAnimals():
    return ["apple", "cat", "спасите"]

