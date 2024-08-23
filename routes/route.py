from fastapi import APIRouter, Request, HTTPException
from models.note import Note
from bson import ObjectId
from config.db import client,collection
from schemas.note import noteEntity, notesEntity, formEnitity

from fastapi.responses import HTMLResponse, RedirectResponse

from fastapi.templating import Jinja2Templates

notes = APIRouter()


templates = Jinja2Templates(directory="templates")

@notes.get("/note", response_class=HTMLResponse)
async def read_note(request: Request):
    try:
        client.admin.command('ping')
        constringr = "Pinged your deployment. You successfully connected to MongoDB!"
    except Exception as e:
        constringr = e

    cursor = collection.find({})
    #datas is list of dictionaries
    datas = await cursor.to_list(length = 100)
    docs = notesEntity(datas)
    return templates.TemplateResponse("notes/note_index.html",{"request":request,"res":constringr,"datas":docs})
    
@notes.post("/note")
async def create_note(request : Request):
    formDict =await formEnitity(request)
    inserted_id = collection.insert_one(formDict)
    return RedirectResponse(url="/", status_code=302)

@notes.get("/edit/{note_id}",response_class=HTMLResponse)
async def edit_note(note_id:str ,request: Request):
    r_id = ObjectId(note_id)
    res = await collection.find_one({"_id": r_id})
    note = noteEntity(res)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return templates.TemplateResponse("notes/edit_note.html", {"request": request, "note": note})


@notes.post("/edit/")
async def update_note(request: Request):
    formDict = await formEnitity(request)
    result = await collection.update_one(
        {"_id": ObjectId(formDict["id"])},
        {"$set": formDict}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return RedirectResponse(url="/note", status_code=302)

@notes.post("/delete/{note_id}")
async def delete_note(note_id: str):
    r_id = ObjectId(note_id)
    result = await collection.delete_one({"_id": r_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Note not found")
    return RedirectResponse(url="/note", status_code=302)


@notes.get('/search/', response_class=HTMLResponse)
async def search_note(query: str, request: Request):
    print(f"Received query: {query}")  # Logging the query for debugging
    try:
        # Use MongoDB's $regex operator to perform a case-insensitive search
        search_query = {
            "$or": [
                {"title": {"$regex": query, "$options": "i"}},
                {"desc": {"$regex": query, "$options": "i"}}
            ]
        }

        cursor = collection.find(search_query)
        results = await cursor.to_list(length=100)

        if not results:
            return templates.TemplateResponse("notes/note_index.html", {"request": request, "res": "No notes found", "datas": []})

        # Convert the result documents to the expected format
        docs = notesEntity(results)
        return templates.TemplateResponse("notes/note_index.html", {"request": request, "res": f"Found {len(docs)} notes", "datas": docs})

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Search failed: {e}")


@notes.get("/item/{item_id}")
def read_id(item_id:int ,q: str|None=None):
    return {"item_id":item_id,"query":q}