from pydantic import BaseModel
from datetime import datetime

class NoteBase(BaseModel):
    title: str
    content : str

class CreateNote(NoteBase):
    user_id:int
    last_modified:datetime

class Note(CreateNote):
    id : int
    class Config:
        orm_mode = True

class EditNote(BaseModel):
    id : int
    title: str = None
    content: str = None
    
class DeleteNote(BaseModel):
    id : int