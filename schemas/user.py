from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# class userDetails(BaseModel):
#     username: str
#     full_name: str
#     age: Optional[int] = None
#     email: str
#     disabled: Optional[bool] = None

# class passwordInDb(userDetails):
#     hashed_pw: str

# class userCreate(BaseModel):
#     username: str
#     password: str

#for mongodb obj to python dict
def userEntity(item) -> dict:
    return {
        "id": item["_id"],
        "username" : item["username"],
        "email" : item["email"],
        "age" : item["age"],
        "full_name" : item["full_name"],
        "hashed_pw" : item["hashed_pw"],
        "disabled" : item["disabled"],
    }

def usersEntity(items) -> list[dict]:
    return [userEntity(item) for item in items]




def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)