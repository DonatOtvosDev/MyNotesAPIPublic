from sqlalchemy.orm import Session

import database.models.db_modells as models
from database.schemas.user_schemas import UserRegister

def create_user(db:Session, user:UserRegister, hashed_password:str) -> models.User:
    db_user = models.User(
        username = user.username,
        hashed_password = hashed_password
    ) 
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def get_user_by_username(db:Session, username:str) -> models.User | None:
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_id(db:Session, id:int) -> models.User | None:
    return db.query(models.User).filter(models.User.id == id).first()


def db_delete_user(db:Session, id:int) -> None:
    db.query(models.User).filter(models.User.id == id).delete()
    db.commit()