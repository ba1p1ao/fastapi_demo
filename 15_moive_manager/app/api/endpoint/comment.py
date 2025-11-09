from fastapi import APIRouter, Depends
from core import deps

from models.comment import Comment
from schemas.comment import CommentCreate

router = APIRouter()

@router.post("/")
async def addComment(comment_data: CommentCreate, current_user=Depends(deps.get_current_user)):
    comment = await Comment.create(
        user_id=current_user.id,
        movie_id=comment_data.movie_id,
        content=comment_data.content,
        rating=comment_data.rating,
    )
    return comment