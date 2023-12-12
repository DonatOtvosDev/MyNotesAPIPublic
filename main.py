from fastapi import FastAPI, Depends, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database.database_services import start_server, get_db

from reps.std_reps.authentication import login_for_access, authenticate, register, delete_user
from reps.std_reps.noteReps import create_note, edit_note, delete_note, get_note

from database.schemas.user_schemas import UserRegister, User
from database.schemas.token_schemas import Token
from database.schemas.note_scemas import NoteBase, Note, EditNote, DeleteNote

start_server()

app = FastAPI()

@app.post("/token", response_model=Token, tags=["User"], status_code=status.HTTP_201_CREATED)
async def login_for_access_token(db:Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    return login_for_access(username=form_data.username, password=form_data.password, db=db)

@app.get("/user", response_model=User, tags=["User"])
async def get_user(current_user : User = Depends(authenticate)):
    return current_user

@app.post("/register", response_model=User, tags=["User"], status_code=status.HTTP_201_CREATED)
async def register_new_user(user:UserRegister, db:Session = Depends(get_db)):
    return register(user=user, db=db)

@app.delete("/deletelogin",tags=["User"], status_code=status.HTTP_202_ACCEPTED)
async def delete_login(user:UserRegister, current_user : User = Depends(authenticate), db:Session = Depends(get_db)):
    return delete_user(user_login=user, user_authed=current_user, db=db)

@app.get("/note/{note_id}",tags=["Notes"])
async def access_note(note_id:int, current_user : User = Depends(authenticate), db:Session = Depends(get_db)):
    return get_note(db=db, user=current_user, note_id=note_id)

@app.post("/createnote", response_model=Note, tags=["Notes"], status_code=status.HTTP_201_CREATED)
async def get_my_notes(note: NoteBase, current_user : User = Depends(authenticate), db:Session = Depends(get_db)):
    return create_note(db=db, user=current_user, note=note)

@app.post("/updatenote", response_model=Note, tags=["Notes"])
async def update_note(note : EditNote, current_user : User = Depends(authenticate), db:Session = Depends(get_db)):
    return edit_note(db=db, user=current_user, note=note)

@app.delete("/deletenote",tags=["Notes"], status_code=status.HTTP_202_ACCEPTED)
async def remove_note(note : DeleteNote, current_user : User = Depends(authenticate), db:Session = Depends(get_db)):
    return delete_note(db=db, note=note, user=current_user)

@app.get("/", tags=["Redirect"])
async def redirect():
    return RedirectResponse(url="/docs")