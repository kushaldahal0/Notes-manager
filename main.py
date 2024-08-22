import os

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
# from pymongo.server_api import ServerApi

from fastapi import FastAPI, Request
from typing import Union
from dotenv import load_dotenv
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI") #+ "&tlsInsecure=true"
client = AsyncIOMotorClient(MONGODB_URI)#, server_api=ServerApi('1'))
database = client.First
collection = database.get_collection("First")

app = FastAPI()

app.mount("/static", StaticFiles(directory = "static"), name='static')
templates = Jinja2Templates(directory="templates")


# Convert MongoDB document to Pydantic model
# def document_to_model(document) -> MyModel:
#     return MyModel(**document)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    
    try:
        client.admin.command('ping')
        constringr = "Pinged your deployment. You successfully connected to MongoDB!"
    except Exception as e:
        constringr = e

    cursor = collection.find({})
    #datas is list of dictionaries
    datas = await cursor.to_list(length = 100)
    docs = [{"id" : data["_id"],"note": data["note"]} for data in datas]
    return templates.TemplateResponse("index.html",{"request":request,"res":constringr,"datas":docs})
    # return {"Hello": "World"}


@app.get("/item/{item_id}")
def read_id(item_id:int ,q: Union[str,None]=None):
    return {"item_id":item_id,"query":q}