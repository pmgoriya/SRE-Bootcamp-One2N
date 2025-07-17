from sqlmodel import create_engine, Session, SQLModel, Field
from dotenv import load_dotenv
import os
from typing import Annotated
from fastapi import Depends
from datetime import datetime, timezone
from sqlalchemy import Column, String

load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"


class Student(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    first_name: str = Field(sa_column=Column(String, nullable=False)) #using fields from sqlalchemy to not import sqlmodel in every migration file at the top.
    last_name: str = Field(sa_column=Column(String, nullable=False))
    email: str = Field(sa_column=Column(String, nullable=False))
    age: int | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc)) # use lambda coz default_factory expects to call a function, each time new instance is created
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))



engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]