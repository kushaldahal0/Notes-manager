from fastapi import APIRouter, Request
from models.note import Note

from config.db import client,collection
from schemas.note import noteEntity, notesEntity

from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates

notes = APIRouter()


templates = Jinja2Templates(directory="templates")

@notes.get("/", response_class=HTMLResponse)
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



@notes.get("/item/{item_id}")
def read_id(item_id:int ,q: str|None=None):
    return {"item_id":item_id,"query":q}