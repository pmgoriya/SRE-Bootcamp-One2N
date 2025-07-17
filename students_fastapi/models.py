from pydantic import BaseModel, Field
from typing import Optional
from database import Student
from datetime import datetime

class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    email: str 
    age: Optional[int] = Field(default=None, ge=5)


class StudentRead(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str 
    age: int | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
# Student object will return class with attributes, while trying to return object pydantic needs to know how to read attributes from objects

class StudentUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    age: int | None = None