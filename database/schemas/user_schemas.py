from pydantic import BaseModel
from database.schemas.note_scemas import Note
class UserBase(BaseModel):
    username : str
    notes : list[Note]

class User(UserBase):
    id : int

class UserRegister(BaseModel):
    username : str
    password : str

