from fastapi import APIRouter, HTTPException
from typing import List
from tortoise.expressions import Q
from models.user import User
from schemas.user import UserCreate, UserLogin
from core import auth, deps

router = APIRouter()


@router.post("/login")
async def login(user_data: UserLogin):
    user = await User.get_or_none(email=user_data.email)

    if not user or not auth.verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="用户名或密码错误")

    token = auth.create_access_token(data={"sub": user.username})
    response = {
        "token": token,
        "token_type": "bearer",
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }
    return response


@router.post("/register")
async def register(user_data: UserCreate):
    user = await User.get_or_none(
        Q(username=user_data.username) | Q(email=user_data.email)
    )

    if user:
        raise HTTPException(status_code=400, detail="用户名或邮箱已存在")

    password_hash = auth.get_password_hash(user_data.password)

    user = await User.create(
        username=user_data.username,
        email=user_data.email,
        password_hash=password_hash,
    )
    return user
