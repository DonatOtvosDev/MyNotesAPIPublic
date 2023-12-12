from sqlalchemy.orm import Session

import database.models.db_modells as models
from database.schemas.note_scemas import CreateNote

def db_create_note(db:Session, note:CreateNote) -> models.Note:
    db_note = models.Note(
        title = note.title,
        content = note.content,
        last_modified = note.last_modified,
        user_id = note.user_id
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)

    return db_note

def db_get_note_by_id(db:Session, id:int) -> models.Note | None:
    return db.query(models.Note).filter(models.Note.id == id).first()

def db_get_note_by_title(db:Session, user_id:int, title:str) -> models.Note | None:
    return db.query(models.Note).filter(models.Note.user_id == user_id).filter(models.Note.title == title).first()

def db_update_note(db:Session, id:int, data_to_update: dict):
    db.query(models.Note).filter(models.Note.id == id).update(data_to_update)
    db.commit()

def db_delete_note(db:Session, id:int):
    db.query(models.Note).filter(models.Note.id == id).delete()
    db.commit()