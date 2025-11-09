from fastapi import APIRouter
from pydantic import BaseModel

teacher = APIRouter()

class Teacher(BaseModel):
    id: int
    name: str
    pwd: str
    tno: int
