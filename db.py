from sqlalchemy import Engine, create_engine
from sqlmodel import SQLModel, Session


def get_engine() -> Engine:
    return create_engine("sqlite:///database.db")


def createdb():
    SQLModel.metadata.create_all(get_engine())

def get_session():
    with Session(get_engine()) as session:
        yield session