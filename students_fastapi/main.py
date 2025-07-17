from fastapi import FastAPI, HTTPException
from database import SessionDep, Student
from sqlmodel import text, select
from models import StudentCreate, StudentRead, StudentUpdate
from datetime import datetime, timezone


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

@app.get("/students/{id}", response_model=StudentRead)
def get_student(id: int, session: SessionDep):
    student = session.get(Student, id)
    if not student:
        raise HTTPException(status_code=404, detail="Student Not Found")
    return student

@app.patch("/students/{id}", response_model=StudentRead)
def update_student(id: int, student_update: StudentUpdate, session: SessionDep):
    student = session.get(Student, id)
    if not student:
        raise HTTPException(status_code=404, detail="Student Not Found")
    student_data = student_update.model_dump(exclude_unset=True) # so that he is not able to pass None and exclude the data which is already present
    student.sqlmodel_update(student_data)

    #manually updating the updated_at
    student.updated_at = datetime.now(timezone.utc)

    session.add(student)
    session.commit()
    session.refresh(student)

    return student


@app.delete("/students/{id}")
def delete_student(id:int, session: SessionDep):
    student = session.get(Student, id)
    if not student:
        raise HTTPException(status_code=404, detail="Student Not Found")
    session.delete(student)
    session.commit()

    return {"ok": True}