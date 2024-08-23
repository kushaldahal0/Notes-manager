from pydantic import BaseModel
from typing import Optional

class userDetails(BaseModel):
    username: str
    full_name: str
    age: Optional[int] = None
    email: str
    disabled: Optional[bool] = None

class passwordInDb(userDetails):
    hashed_pw: str

class userCreate(BaseModel):
    username: str
    password: str