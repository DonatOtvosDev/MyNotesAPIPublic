from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import re

from database.secret import SECRET_KEY

from database.database_services import get_db

from database.schemas.user_schemas import UserRegister, User

from reps.db_reps.db_user import get_user_by_username, create_user, db_delete_user
from reps.db_reps.db_notes import db_delete_note


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(password:str, hashed_password:str):
    return pwd_context.verify(password, hashed_password)

def login_for_access(username:str, password:str, db:Session):
    incorrect_login = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = get_user_by_username(db=db, username=username)

    if user == None:
        raise incorrect_login
    if not verify_password(password=password, hashed_password=user.hashed_password):
        raise incorrect_login

    expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"sub":username, "expires":expires.isoformat()}

    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": access_token, "token_type": "bearer", "expiary" : expires}


def authenticate(db:Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        expires : datetime = datetime.fromisoformat(payload.get("expires"))
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
       
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(username=username, db=db)
    if user is None:
        raise credentials_exception
    if datetime.utcnow() > expires:
        raise credentials_exception

    return User(
        id=user.id,
        username=user.username,
        notes=user.notes
    )


def register(user: UserRegister, db: Session):
    if get_user_by_username(db=db, username=user.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username is already in use"
        )
    if len(user.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Password is too short it must be 6 characters"
        )
    
    if len(re.findall(pattern="[^a-z0-9]", string=user.username)) > 0 or len(user.username) < 4:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, 
            detail="Username is not acceptable"
        )
    
    user = create_user(db=db, user=user, hashed_password=pwd_context.hash(user.password))

    return User(
        id=user.id,
        username=user.username,
        notes=user.notes
    )

def delete_user(user_login:UserRegister, user_authed: User, db:Session):
    if user_login.username != user_authed.username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials")
    
    user = get_user_by_username(username=user_login.username, db=db)
    if user == None or not verify_password(password=user_login.password, hashed_password=user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    for note in user.notes:
        db_delete_note(db=db, id=note.id)

    db_delete_user(db=db, id=user.id)

    return "User successfully removed"