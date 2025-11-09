from fastapi import APIRouter
from pydantic import BaseModel
from routers.teacher import Teacher
Course = APIRouter()

class Course(BaseModel):
    id: int
    name: str
    teacher: Teacher
    addr: str