from pydantic import BaseModel
from typing import List

class StudentInput(BaseModel):
    answers: List[int]
