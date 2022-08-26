from lib2to3.pytree import Base
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

fakedb = []

class Course(BaseModel):
    id: int
    name: str
    price: int
    is_early_bird: Optional[bool] = None



@app.get("/")
def read_root():
    return {"grettings":" welcome to the World!!"}

# If I write /docs it will show the swagger version where I can try and test

@app.get("/courses")
def get_courses():
    return fakedb

@app.get("/courses/{course_id}")
def get_a_course(course_id: int):
    course = course_id -1
    return fakedb[course]

@app.post("/courses")
def add_course(course: Course):
    fakedb.append(course.dict())
    return fakedb[-1]

@app.delete("/courses/{course_id}")
def delete_course(course_id: int):
    fakedb.pop(course_id -1)
    return {"task": "Deletion successful"}