from sqlalchemy import Engine, create_engine, URL
from sqlmodel import SQLModel, Session
import os


def get_engine() -> Engine:
    url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
    )
    return create_engine(url, echo=True)


def createdb():
    SQLModel.metadata.create_all(get_engine())


def get_session():
    with Session(get_engine()) as session:
        yield session
