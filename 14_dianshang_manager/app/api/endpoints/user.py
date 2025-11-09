from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import Response
from models.user import User
from schemas.user import Token, UserCreate, UserLogin, UserResponse, UserUpdate
from core import auth, dependencies

router = APIRouter()


@router.post("/auth/register")
async def addUser(user_data: UserCreate):
    user = await User.filter(username=user_data.username).first()
    if user:
        raise HTTPException(
            status_code=400, detail=f"用户名：{user_data.username} 已存在"
        )

    user = await User.filter(email=user_data.email).first()
    if user:
        raise HTTPException(status_code=400, detail=f"邮箱：{user_data.email} 已存在")

    # 创建用户
    password_hash = auth.get_password_hash(user_data.password)
    user = await User.create(
        username=user_data.username,
        email=user_data.email,
        hashed_password=password_hash,
    )
    return user


@router.post("/auth/login", response_model=Token)
async def login(user_data: UserLogin):
    user = await User.filter(username=user_data.username, is_active=True).first()

    if not user or not auth.verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="用户名或密码错误")

    token = auth.create_access_token(data={"sub": user.username})
    response = {
        "access_token": token,
        "token_type": "bearer",
        "user": user,
    }
    return response


@router.get("/users/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(dependencies.get_current_user)):
    """获取当前登录用户信息"""
    return current_user

@router.put("/users/me")
async def updateUser(user_data: UserUpdate, current_user: User = Depends(dependencies.get_current_user)):
    args = user_data.model_dump(include=["email"])

    exist_email = await User.filter(email=args["email"])
    # 验证邮箱是否已经存在
    if exist_email:
        raise HTTPException(status_code=400, detail=f"邮箱：{user_data.email} 已存在")
    # print(args)    
    current_user.email = args["email"]
    user = await current_user.save()
    return user

@router.put("/users/me/password")
async def updateUserPassword(user_data: UserUpdate, current_user: User = Depends(dependencies.get_current_user)):
    args = user_data.model_dump(include=["old_password", "new_password"])

    # 验证旧密码是不是用户原登录密码
    if not auth.verify_password(args["old_password"], current_user.hashed_password):
        raise HTTPException(status_code=400, detail="旧密码与原密码不一致")
    # print(args)
    password_hash = auth.get_password_hash(args["new_password"])
    current_user.hashed_password = password_hash
    user = await current_user.save()
    return user