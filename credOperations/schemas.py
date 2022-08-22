from pydantic import BaseModel
from typing import Optional

class course(BaseModel):
    id: int
    name: str
    price: int
    is_early_bird: Optional[bool] = None