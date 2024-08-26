from fastapi import APIRouter, Request, HTTPException, Depends
from models.note import Note
from models.token import Token, TokenData
from bson import ObjectId
from config.db import client, collection
from schemas.note import noteEntity, notesEntity, formEntity
from schemas.user import verify_access_token
from routes.user import get_current_user
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

notes = APIRouter()
templates = Jinja2Templates(directory="templates")

# Middleware to ensure MongoDB connection
@notes.get("/note", response_class=HTMLResponse)
async def read_note(request: Request, 
                    current_user: TokenData = Depends(get_current_user)):
    try:
        client.admin.command('ping')
        constringr = "Pinged your deployment. You successfully connected to MongoDB!"
    except Exception as e:
        constringr = str(e)

    cursor = collection.find({})
    datas = await cursor.to_list(length=100)
    docs = notesEntity(datas)
    return templates.TemplateResponse("notes/note_index.html", {"request": request,
                                                                "res": constringr,
                                                                "datas": docs,
                                                                "current_user":current_user.username})

@notes.post("/note")
async def create_note(request: Request,
                        current_user: TokenData = Depends(get_current_user)):
    formDict = await formEntity(request)
    inserted_id = collection.insert_one(formDict).inserted_id
    return RedirectResponse(url="/note", status_code=302)

@notes.get("/edit/{note_id}", response_class=HTMLResponse)
async def edit_note(note_id: str, request: Request,
                     current_user: TokenData = Depends(get_current_user)):
    r_id = ObjectId(note_id)
    res = await collection.find_one({"_id": r_id})
    note = noteEntity(res)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return templates.TemplateResponse("notes/edit_note.html", {"request": request,
                                                                "note": note,
                                                                "current_user":current_user.username})

@notes.post("/edit/")
async def update_note(request: Request, 
                        current_user: TokenData = Depends(get_current_user)):
    formDict = await formEntity(request)
    result = await collection.update_one(
        {"_id": ObjectId(formDict["id"])},
        {"$set": formDict}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Note not found")
    return RedirectResponse(url="/note", status_code=302)

@notes.post("/delete/{note_id}")
async def delete_note(note_id: str,
                     current_user: TokenData = Depends(get_current_user)):
    r_id = ObjectId(note_id)
    result = await collection.delete_one({"_id": r_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Note not found")
    return RedirectResponse(url="/note", status_code=302)

@notes.get('/search/', response_class=HTMLResponse)
async def search_note(query: str, request: Request, 
                        current_user: TokenData = Depends(get_current_user)):
    try:
        search_query = {
            "$or": [
                {"title": {"$regex": query, "$options": "i"}},
                {"desc": {"$regex": query, "$options": "i"}}
            ]
        }

        cursor = collection.find(search_query)
        results = await cursor.to_list(length=100)

        if not results:
            return templates.TemplateResponse("notes/note_index.html", {"request": request,
                                                                        "res": "No notes found",
                                                                        "datas": [],
                                                                        "current_user":current_user.username})

        docs = notesEntity(results)
        return templates.TemplateResponse("notes/note_index.html", {"request": request,
                                                                    "res": f"Found {len(docs)} notes",
                                                                    "datas": docs,
                                                                    "current_user":current_user.username})

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Search failed: {e}")
