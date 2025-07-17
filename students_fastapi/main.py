from fastapi import FastAPI
from database import SessionDep
from sqlmodel import text


app = FastAPI()

@app.get("/students")
async def get_students(session: SessionDep):
    # return {"message": "You will get students on here later"}
    return session.exec(text("SELECT 1"))
