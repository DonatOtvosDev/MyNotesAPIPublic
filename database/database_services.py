import database.models.db_modells as models
from database.database import engine, SessionLocal

def start_server():
    models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
