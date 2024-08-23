from fastapi import APIRouter, Request, HTTPException
from models.user import userDetails, passwordInDb, userCreate
from bson import ObjectId
from config.db import client,user_collection
from schemas.note import noteEntity, notesEntity, formEnitity

from fastapi.responses import HTMLResponse, RedirectResponse

from fastapi.templating import Jinja2Templates

user = APIRouter()


templates = Jinja2Templates(directory="templates")

@user.get("/", response_class=HTMLResponse)
def user_login(request: Request):
    context = {"request":request}
    return templates.TemplateResponse("users/user_index.html",context)