from fastapi import APIRouter, Depends
from models.models import User, File
from core import auth, deps
from schemas.user import UserBase
router = APIRouter()


@router.get("/me", response_model=UserBase)
async def getMe(current_user: User = Depends(deps.get_current_user)):

    return current_user


@router.get("/me/files")
async def getMeFiles(current_user: User = Depends(deps.get_current_user)):
    files = await File.filter(author_id=current_user.id).prefetch_related('author')
    return files