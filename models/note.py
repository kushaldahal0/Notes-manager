from pydantic import BaseModel

class Note(BaseModel):
    title : str
    desc : str
    imporant: bool