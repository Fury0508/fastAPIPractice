from pydantic import BaseModel
from typing import List, Optional

class course(BaseModel):
    course_name: str
    course_fee: int
    is_early_bird: Optional[bool] = None
    class Config():
        orm_mode = True


class Users(BaseModel):
    name :str
    email : str
    password : str

class ShowUsers(BaseModel):
    name :str
    email : str
    course_taken : List[course]

    class Config():
        orm_mode = True

class showCourse(BaseModel):
    course_name: str
    course_fee: int
    # is_early_bird: Optional[bool] = None
    studentname: ShowUsers
    

    class Config():
        orm_mode = True