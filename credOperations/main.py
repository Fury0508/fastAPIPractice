
from pyexpat import model
import re
from fastapi import Depends, FastAPI, Response,HTTPException
from database import SessionLocal
import schemas
import models
from database import engine
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import hashing
app = FastAPI()


models.Base.metadata.create_all(engine) 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@app.post("/courses",status_code=201,tags=['Courses'])
def create(request:schemas.course, db:Session = Depends(get_db)):
    # the value of student is hardcorded I have to change this 
    #need to go through the documentation for that 
    new_course = models.course(course_name = request.course_name,course_fee = request.course_fee,is_early_bird = request.is_early_bird,student_id = 1)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

@app.get("/get_course",tags=['Courses'])
def get_course(db:Session = Depends(get_db)):
    courses = db.query(models.course).all()
    return courses

#############################   
# response_model = schemas.show_course is not working I have to look into this later 
########################
@app.get('/get_a_course/{id}',response_model= schemas.showCourse,status_code=200,tags=['Courses'])
def get_a_course(id,db:Session = Depends(get_db)):
    courses = db.query(models.course).filter(models.course.id == id).first()
    
    if not courses:
        raise HTTPException(status_code=404,detail="Course not present")
        # response.status_code = 404
        # return {"Error": "Course not present"}
    return courses

@app.delete("/delete_course/{id}",tags=['Courses'])
def delete_course(id,db: Session = Depends(get_db)):
    db.query(models.course).filter(models.course.id == id).delete(synchronize_session=False)
    db.commit()
    
    return {"details":"course is deleted from the database"}

@app.put("/course/{id}",status_code = 202,tags=['Courses'])
def update_course(id,request:schemas.course,db:Session = Depends(get_db)):
    
    courses = db.query(models.course).filter(models.course.id == id)
    if not courses.first():
        raise HTTPException(status_code = 404,detail={"Error":"course id is not present"})
        
    courses.update(values={"course_name":request.course_name,"course_fee":request.course_fee})
    db.commit()
    return {"details":"data is updated"}

# creating user


@app.post("/user",response_model=schemas.ShowUsers,tags=['Users'])
def create_user(request: schemas.Users,db:Session = Depends(get_db)):
   
    new_user = models.User(name = request.name,email = request.email,password = hashing.Hash.encrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/user/{id}",response_model = schemas.ShowUsers,tags=['Users'])
def get_users(id: int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404,detail={"Error":"User not present"})
    return user