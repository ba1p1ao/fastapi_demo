from fastapi import APIRouter, Request, HTTPException, status, Depends
from fastapi.responses import Response

from models.models import User
from schemas.user import Token, UserCreate, UserResponse
from core.dependencies import get_current_user
from core.auth import get_password_hash, create_access_token, verify_password


router_user = APIRouter()


@router_user.post("/auth/register", response_model=UserResponse)
async def addUser(user_data: UserCreate):
    existing_user = await User.filter(username=user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在",
        )

    if user_data.email:
        existing_user_email = await User.filter(email=user_data.email).first()
        if existing_user_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户邮箱已存在",
            )
    # 创建用户
    print("===========")
    hash_password = get_password_hash(user_data.password)
    print(hash_password)
    user = await User.create(
        username=user_data.username,
        password_hash=hash_password,
        email=user_data.email,
    )
    return user


@router_user.post("/auth/login", response_model=Token)
async def login(user_data: UserCreate):
    user = await User.filter(username=user_data.username).first()
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名或密码错误",
        )
    
    # 创建访问令牌
    access_token = create_access_token(
        data={"sub": user.username}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

# 获取当前用户信息
@router_user.get("/auth/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """获取当前登录用户信息"""
    print("me")
    return current_user