from fastapi import APIRouter
from pydantic import BaseModel

clas = APIRouter()

class Clas(BaseModel): 
    name: str
