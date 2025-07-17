from fastapi import FastAPI, HTTPException, APIRouter
from database import SessionDep, Student
from sqlmodel import text, select
from models import StudentCreate, StudentRead, StudentUpdate
from datetime import datetime, timezone
from logging_config import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI()
v1_router = APIRouter(prefix="/api/v1")


@v1_router.get("/students", response_model=list[StudentRead])
def get_students(session: SessionDep):
    logger.info("Fetching all students from the database")
    students = session.exec(select(Student)).all()
    logger.debug(f"Retrieved {len(students)} students")

    return students


@v1_router.post("/students", response_model=StudentRead)
def create_student(student: StudentCreate, session: SessionDep):
    logger.info(f"Creating a new student with email: {student.email}")
    new_student = Student(**student.model_dump())
    session.add(new_student)
    session.commit()
    session.refresh(new_student)
    logger.debug(f"Student created with ID: {new_student.id}")

    return StudentRead.model_validate(new_student.model_dump())

@v1_router.get("/students/{id}", response_model=StudentRead)
def get_student(id: int, session: SessionDep):
    logger.info(f"Fetching student with ID: {id}")
    student = session.get(Student, id)
    if not student:
        logger.warning(f"Student with ID {id} not found")
        raise HTTPException(status_code=404, detail="Student Not Found")
    return student

@v1_router.patch("/students/{id}", response_model=StudentRead)
def update_student(id: int, student_update: StudentUpdate, session: SessionDep):
    logger.info(f"Updating student with ID: {id}")
    student = session.get(Student, id)
    if not student:
        logger.warning(f"Student with ID {id} not found")
        raise HTTPException(status_code=404, detail="Student Not Found")
    student_data = student_update.model_dump(exclude_unset=True) # so that he is not able to pass None and exclude the data which is already present
    logger.debug(f"Update data: {student_data}")

    student.sqlmodel_update(student_data)

    #manually updating the updated_at
    student.updated_at = datetime.now(timezone.utc)

    session.add(student)
    session.commit()
    session.refresh(student)

    logger.info(f"Student with ID {id} updated successfully")

    return student


@v1_router.delete("/students/{id}")
def delete_student(id:int, session: SessionDep):
    logger.info(f"Deleting student with ID: {id}")
    student = session.get(Student, id)
    if not student:
        logger.warning(f"Student with ID {id} not found")
        raise HTTPException(status_code=404, detail="Student Not Found")
    session.delete(student)
    logger.info(f"Student with ID {id} deleted")
    session.commit()

    return {"ok": True}

@v1_router.get("/healthcheck")
def healthcheck(session: SessionDep):
    logger.info("Healthcheck endpoint called")
    try:
        session.exec(select(Student).limit(1)).first()
        logger.info("Database connection is healthy")
        return {"status": "ok", "db": "connected"}
    except Exception as e:
        logger.error(f"Healthcheck failed: {e}")
        return {"status": "error", "db": "disconnected"}