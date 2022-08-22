from typing import Counter
from database import Base
from sqlalchemy import Column,Integer, String, Boolean, null
from typing import Optional

class course(Base):
    __tablename__ = "coursedetails"
    id = Column(Integer,primary_key = True,index = True)
    course_name = Column(String,nullable=True)
    course_fee = Column(Integer,nullable=True)
    is_early_bird = Column(Boolean,nullable = False)

