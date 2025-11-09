from fastapi import APIRouter, Depends
from tortoise.expressions import  Q
from models.models import Users, Files
from schemas.user import UserResponse
from schemas.file import FileResponseSchemas
from core import deps
from config import SORT_DICT
import math

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def getMe(current_user: Users = Depends(deps.get_current_user)):
    return current_user


@router.get("/me/files", response_model=FileResponseSchemas)
async def getMeFiles(
    path: str = "/",
    page: int = 1,
    page_size: int = 20,
    sort: str = "name",
    order: str = "asc",
    q: str = "",
    current_user: Users = Depends(deps.get_current_user),
):

    skip = (page - 1) * page_size
    order_prefix = "" if order == "asc" else "-"
    if q:
        files = (
            await Files.filter(Q(name__icontains=q) & Q(is_directory=False))
            .order_by(f"{order_prefix}{SORT_DICT[sort]}")
            .offset(skip)
            .limit(page_size)
        )
    else:
        files = (
            await Files.filter(Q(owner_id=current_user.id) & Q(is_directory=False))
            .order_by(f"{order_prefix}{SORT_DICT[sort]}")
            .offset(skip)
            .limit(page_size)
        )
    response_data = {
        "files": files,
        "path": path,
        "total": len(files),
        "page": page,
        "pages": math.ceil(len(files) / page_size),
    }

    return response_data
