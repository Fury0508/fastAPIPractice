from typing import Counter
from database import Base
from sqlalchemy import Column,Integer, String, Boolean, ForeignKey
from typing import Optional
from sqlalchemy.orm import relationship

class course(Base):
    __tablename__ = "coursedetails"
    id = Column(Integer,primary_key = True,index = True)
    course_name = Column(String,nullable=True)
    course_fee = Column(Integer,nullable=True)
    is_early_bird = Column(Boolean,nullable = False)
    student_id = Column(Integer,ForeignKey("users.id"))
    studentname  = relationship("User",back_populates = 'course_taken')

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key = True, index = True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    course_taken = relationship('course',back_populates = 'studentname')