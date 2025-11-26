from sqlmodel import create_engine, Session, SQLModel
from src.core.config import CONFIG

engine = create_engine(CONFIG.DB_URL, echo=False)

def get_engine():
    return engine

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
