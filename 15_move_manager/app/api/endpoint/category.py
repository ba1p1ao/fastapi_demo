from fastapi import APIRouter
from models.category import Category


router = APIRouter()

@router.get("/")
async def getAllCatergories():
    categories = await Category.all()
    return categories
