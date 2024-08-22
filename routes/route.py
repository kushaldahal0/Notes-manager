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
    # docs = [{"id" : data["_id"],"title": data["title"], "desc": data["desc"], "important": data["important"]} for data in datas]
    docs = notesEntity(datas)
    return templates.TemplateResponse("index.html",{"request":request,"res":constringr,"datas":docs})

@notes.post("/")
async def create_note(request : Request):
    form = await request.form()
    print(form)
    formDict = dict(form)
    print(formDict)
    formDict["important"] = True if formDict.get("important") == "on" else False
    inserted_note = collection.insert_one(formDict)
    return 

@notes.get("/item/{item_id}")
def read_id(item_id:int ,q: str|None=None):
    return {"item_id":item_id,"query":q}