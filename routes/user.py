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

@user.post("/")
async def check_user(request: Request):
    form = await request.form()
    try:
        #already on dict
        db_user = await user_collection.find_one({"username": form["username"]})
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        if not verify_password(form["password"], db_user["hashed_password"]):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

        if db_user["disabled"]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User account disabled")

        return RedirectResponse("/note", status_code=status.HTTP_200_OK)
    
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
    context = {"request": request}

    if formDict['password'] != formDict['confirm_password']:
        context["Status"]: "Passwords do not match"
        return RedirectResponse("/signup", context ,status_code=status.HTTP_409_CONFLICT)

    formDict["hashed_password"] = get_password_hash(formDict['password'])
    formDict["disabled"] = False
    del formDict['password']  # Remove plain text password from the dictionary
    del formDict['confirm_password']  # Remove confirm password field from the dictionary
    
    try:
        await user_collection.insert_one(formDict)
        return RedirectResponse("/index", status_code=status.HTTP_200_OK)
    except DuplicateKeyError:
        context["Status"]: "Username already exists"
        raise HTTPException(status_code=400, detail="Username already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
    return templates.TemplateResponse("users/signup.html", context)

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

