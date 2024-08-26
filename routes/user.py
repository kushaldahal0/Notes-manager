from fastapi import APIRouter, Request, HTTPException, status, Depends
from models.user import userDetails, passwordInDb
from models.token import Token, TokenData
from bson import ObjectId
from config.db import client,user_collection
from schemas.user import userEntity, usersEntity, get_password_hash, verify_password, create_access_token, verify_access_token
from pymongo.errors import DuplicateKeyError
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

user = APIRouter()


templates = Jinja2Templates(directory="templates")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(request: Request) -> TokenData:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return TokenData(username=username)


@user.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@user.get("/", response_class=HTMLResponse)
def user_login(request: Request):
    context = {"request":request}
    return templates.TemplateResponse("users/user_index.html",context)

@user.post("/", response_class=HTMLResponse)
async def user_login(request: Request):
    form = await request.form()
    try:
        db_user = await user_collection.find_one({"username": form["username"]})
        if not db_user:
            return templates.TemplateResponse("users/user_index.html", {"request": request, "Status": "User not found"})

        if not verify_password(form["password"], db_user["hashed_password"]):
            return templates.TemplateResponse("users/user_index.html", {"request": request, "Status": "Incorrect password"})

        if db_user["disabled"]:
            return templates.TemplateResponse("users/user_index.html", {"request": request, "Status": "User account disabled"})

        # Create JWT token
        access_token = create_access_token(data={"sub": db_user["username"]})

        # print(access_token)
        # Redirect with JWT token in response headers
        response = RedirectResponse("/note", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        return response
    
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
        # Create JWT token
        access_token = create_access_token(data={"sub": formDict["username"]})

        # Redirect with JWT token in response headers
        response = RedirectResponse("/note", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        return response

    except DuplicateKeyError:
        return templates.TemplateResponse("users/signup.html", {"request": request, "Status": "Username already exists"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@user.get("/logout")
async def logout(response: RedirectResponse):
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="access_token")
    return response

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

