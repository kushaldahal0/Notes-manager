from fastapi import APIRouter, Request, HTTPException
from models.user import userDetails, passwordInDb, userCreate
from bson import ObjectId
from config.db import client,user_collection
from schemas.user import userEntity, usersEntity, get_password_hash, verify_password

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
        print(form["username"])
        db = await user_collection.find_one({"username"} == form["username"])
        if(db == None):
            res = "no match found in the database!"
            return{"status":res}
        db_user = userEntity(db)
        if verify_password(form["password"], db_user["hashed_password"]):
            res ="login success!!!!"
            if db_user["disabled"] == True:
                res += " but your acc has been disabled!"
        else:
            res = "Login failed"
    except Exception as e:
        res = str(e)
    return{"status":res}


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

