from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import re

from datetime import datetime

from database.schemas.user_schemas import User
from database.schemas.note_scemas import Note, NoteBase, CreateNote, EditNote, DeleteNote

from reps.db_reps.db_notes import db_create_note, db_get_note_by_title, db_get_note_by_id, db_update_note, db_delete_note

VALIDATION_ERROR = HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail= "The data sent is invalid"
    )

def __check_ownership(db:Session, id:int, user_id:int) -> Note:
    db_note = db_get_note_by_id(db=db, id=id)
    if db_note == None or db_note.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note with this id not found"
            )
    
    if db_note.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Note is not owned by user"
        )
    return db_note

def create_note(db:Session, user: User, note:NoteBase ) -> Note:
    if db_get_note_by_title(db=db, user_id=user.id, title=note.title):
        raise VALIDATION_ERROR

    if len(note.title) == 0:
        raise VALIDATION_ERROR
    
    if len(re.findall(pattern="[^a-zA-z0-9áéíóöőúüűÁÉÍÓÖŐÚÜŰ ]", string=note.title)):
       raise VALIDATION_ERROR

    note_data = CreateNote(
        user_id=user.id,
        title=note.title,
        content=note.content,
        last_modified=datetime.now()
    )

    db_note = db_create_note(db=db, note=note_data)

    return db_note

def edit_note(db:Session, user: User, note: EditNote) -> Note:
    __check_ownership(db=db,id=note.id, user_id=user.id)
    
    data_to_update = {}
    if note.title != None:
        if len(note.title) == 0:
            raise VALIDATION_ERROR

        if len(re.findall(pattern="[^a-zA-z0-9áéíóöőúüűÁÉÍÓÖŐÚÜŰ ]", string=note.title)):
            raise VALIDATION_ERROR
        
        if db_get_note_by_id(db=db, id=note.id) == None:
            raise VALIDATION_ERROR 

        data_to_update["title"] = note.title

    if note.content != None:
        data_to_update["content"] = note.content

    data_to_update["last_modified"] = datetime.now()

    db_update_note(db=db, id=note.id, data_to_update=data_to_update)

    db_note = db_get_note_by_id(db=db, id=note.id)
    keys = list(data_to_update.keys())

    if len(keys) < 2:
        raise VALIDATION_ERROR

    if ("title" in keys and db_note.title != note.title) or ("content" in keys and db_note.content != note.content):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Note failed to update"
        )

    return db_note

def get_note(db:Session, note_id:int, user:User):
    note = __check_ownership(db=db, id=note_id, user_id=user.id)
    return note

def delete_note(db:Session, note:DeleteNote, user:User):
    __check_ownership(db=db,id=note.id, user_id=user.id)
    db_delete_note(db=db, id=note.id)

    if db_get_note_by_id(db=db, id=note.id):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Note failed to delete"
        )