from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



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

#jwt tokens creationg and decoding
SECRET_KEY = "KUSHAL"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload if payload else None
    except jwt.PyJWTError:
        return None


