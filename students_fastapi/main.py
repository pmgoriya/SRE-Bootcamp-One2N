from fastapi import FastAPI
from database import SessionDep, Student
from sqlmodel import text, select
from models import StudentCreate, StudentRead
# from datetime import datetime, timezone


app = FastAPI()

@app.get("/students", response_model=list[StudentRead])
def get_students(session: SessionDep):
    students = session.exec(select(Student)).all()

    return students


@app.post("/students", response_model=StudentRead)
def create_student(student: StudentCreate, session: SessionDep):
    new_student = Student(**student.model_dump())
    session.add(new_student)
    session.commit()
    session.refresh(new_student)
    
    return StudentRead.model_validate(new_student.model_dump())