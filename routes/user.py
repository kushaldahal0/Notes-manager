from fastapi import APIRouter, Request, HTTPException, status
from models.user import userDetails, passwordInDb, userCreate
from bson import ObjectId
from config.db import client,user_collection
from schemas.user import userEntity, usersEntity, get_password_hash, verify_password
from pymongo.errors import DuplicateKeyError
from fastapi.responses import HTMLResponse, RedirectResponse

from fastapi.templating import Jinja2Templates

user = APIRouter()


templates = Jinja2Templates(directory="templates")

@user.get("/", response_class=HTMLResponse)
def user_login(request: Request):
    context = {"request":request}
    return templates.TemplateResponse("users/user_index.html",context)

@user.post("/", response_class=HTMLResponse)
async def check_user(request: Request):
    form = await request.form()
    try:
        db_user = await user_collection.find_one({"username": form["username"]})
        if not db_user:
            return templates.TemplateResponse("users/user_index.html", {"request": request, "Status": "User not found"})

        if not verify_password(form["password"], db_user["hashed_password"]):
            return templates.TemplateResponse("users/user_index.html", {"request": request, "Status": "Incorrect password"})

        if db_user["disabled"]:
            return templates.TemplateResponse("users/user_index.html", {"request": request, "Status": "User account disabled"})

        return RedirectResponse("/note", status_code=status.HTTP_302_FOUND)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@user.get("/signup",response_class=HTMLResponse)
async def user_signup(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("users/signup.html",context)

@user.post("/signup", response_class=HTMLResponse)
async def user_signup(request: Request):
    form = await request.form()
    formDict = dict(form)
    
    if formDict['password'] != formDict['confirm_password']:
        # Display error on the same page
        return templates.TemplateResponse("users/signup.html", {"request": request, "Status": "Passwords do not match"})

    formDict["hashed_password"] = get_password_hash(formDict['password'])
    formDict["disabled"] = False
    del formDict['password']
    del formDict['confirm_password']
    
    try:
        await user_collection.insert_one(formDict)
        return RedirectResponse("/note", status_code=status.HTTP_302_FOUND)
    except DuplicateKeyError:
        return templates.TemplateResponse("users/signup.html", {"request": request, "Status": "Username already exists"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user.get("/fakeacc")
async def user_fake(request: Request):
#     fake_users_db = {
#     "johndoe": {
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": get_password_hash("secret"),
#         "disabled": False,
#     }
# }
    fake = {}
    fake["username"] = "johndoe"
    fake["full_name"] = "John Doe"
    fake["email"] = "johndoe@example.com"
    fake["hashed_password"] = get_password_hash("secret")
    fake["disabled"] = False

    inserted_id = await user_collection.insert_one(fake)
    # return {"Sucess":True, "inserted_id":userEntity(inserted_id)}
    return {"Success":True}

