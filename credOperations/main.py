
import re
from fastapi import Depends, FastAPI, Response,HTTPException
from database import SessionLocal
import schemas
import models
from database import engine
from sqlalchemy.orm import Session

app = FastAPI()


models.Base.metadata.create_all(engine) 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@app.post("/courses",status_code=201)
def create(request:schemas.course, db:Session = Depends(get_db)):
    new_course = models.course(course_name = request.name,course_fee = request.price,is_early_bird = request.is_early_bird)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

@app.get("/get_course")
def get_course(db:Session = Depends(get_db)):
    courses = db.query(models.course).all()
    return courses

@app.get("/get_a_course/{id}",status_code=200)
def get_a_course(id,response: Response,db:Session = Depends(get_db)):
    courses = db.query(models.course).filter(models.course.id == id).all()
    if not courses:
        raise HTTPException(status_code=404,detail="Course not present")
        # response.status_code = 404
        # return {"Error": "Course not present"}
    return courses

@app.delete("/delete_course/{id}")
def delete_course(id,db: Session = Depends(get_db)):
    db.query(models.course).filter(models.course.id == id).delete(synchronize_session=False)
    db.commit()
    
    return {"details":"course is deleted from the database"}

@app.put("/course/{id}",status_code = 202)
def update_course(id,request:schemas.course,db:Session = Depends(get_db)):
    
    courses = db.query(models.course).filter(models.course.id == id)
    if not courses.first():
        raise HTTPException(status_code = 404,detail={"Error":"course id is not present"})
        
    courses.update(values={"course_name":request.name,"course_fee":request.price})
    db.commit()
    return {"details":"data is updated"}

 