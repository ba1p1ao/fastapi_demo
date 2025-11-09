from fastapi import APIRouter, HTTPException
from tortoise.expressions import Q
from models.models import File, Comment, User
from schemas.files import FileSearch
from typing import Optional

router = APIRouter()


@router.get("/")
async def getAllfiles(
    page: int = 1,
    keyword: Optional[str] = "",
    category: Optional[str] = "",
    subcategory: Optional[str] = "",
):
    """获取文件的接口"""
    files = await File.filter(
        Q(name__icontains=keyword)
        | Q(description__icontains=keyword)
        & Q(category__icontains=category)
        & Q(subcategory__icontains=subcategory)
    )

    response_data = {"files": files, "total_page": len(files)}

    return response_data


@router.get("/hot")
async def getHotFiles(category: Optional[str] = "game"):
    """获取热门文件的接口"""
    files = await File.filter().order_by("-download_count").limit(10)
    return files


@router.get("/{file_id}")
async def getFileComments(file_id: int):
    """获取单个文件的接口"""
    file = await File.get_or_none(id=file_id)
    if not file:
        raise HTTPException(status_code=404, detail="文件未找到")
    return file


@router.get("/{file_id}/comments")
async def getFileComments(file_id: int):
    """获取单个文件的评论接口"""
    file = await File.get_or_none(id=file_id)
    if not file:
        raise HTTPException(status_code=404, detail="文件未找到")
    comments = await Comment.filter(file_id=file_id).order_by("-created_at")
    response_data = []
    for comment in comments:
        user = await User.get_or_none(id=comment.user_id).values("username")
        print(user)
        if not user:
            continue
        response_data.append(
            {
                "content": comment.content,
                "created_at": comment.created_at,
                "user": user,
            }
        )

    return response_data
