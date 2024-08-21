import os
from pymongo import MongoClient
from fastapi import FastAPI, Request
from typing import Union
from dotenv import load_dotenv
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
conn = MongoClient(MONGODB_URI)

app = FastAPI()

app.mount("/static", StaticFiles(directory = "static"), name='static')
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    try:
        conn.admin.command('ping')
        constringr = "Pinged your deployment. You successfully connected to MongoDB!"
    except Exception as e:
        constringr = e
    return templates.TemplateResponse("index.html",{"request":request,"res":constringr})
    # return {"Hello": "World"}


@app.get("/item/{item_id}")
def read_id(item_id:int ,q: Union[str,None]=None):
    return {"item_id":item_id,"query":q}