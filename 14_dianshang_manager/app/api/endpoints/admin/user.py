from fastapi import APIRouter, HTTPException, Depends
from typing import List
from core import dependencies
from models.user import User
from schemas.user import UserResponse


router = APIRouter()


@router.get("/users", response_model=List[UserResponse])
async def getAllUser(current_user: User = Depends(dependencies.get_admin_user)):
    users = await User.all()
    return users

@router.put("/users/{user_id}")
async def updateUserActive(user_id: int, current_user: User = Depends(dependencies.get_admin_user)):
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=400, detail="用户不存在")
    if user.username == "admin":
        raise HTTPException(status_code=400, detail="管理员不能禁用")
    user.is_active = not user.is_active
    user = await user.save()

    return await getAllUser(current_user)
