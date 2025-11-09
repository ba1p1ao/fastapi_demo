from fastapi import APIRouter, HTTPException, Request, Body
from fastapi.responses import RedirectResponse
from tortoise.expressions import Q
from models.models import User
from schemas.user import UserBase, UserCreate, Token, UserLogin, ResetEmail, VaildateResetToken, ResetPasswordSchemas
from core import auth


router = APIRouter()


@router.post("/login", response_model=Token)
async def login(req_data: UserLogin):
    user = await User.get_or_none(username=req_data.username)
    if not user or not auth.verify_password(req_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    token = auth.create_access_token(data={"sub": str(user.id)})
    print(token)
    response_data = {"access_token": token, "token_type": "bearer", "user": user}
    return response_data


@router.post("/register", response_model=Token)
async def register(req_data: UserCreate):
    print(req_data)
    user = await User.filter(Q(username=req_data.username) | Q(email=req_data.email)).first()
    if user:
        if user.username == req_data.username:
            raise HTTPException(status_code=400, detail="用户名已存在")
        if user.email == req_data.email:
            raise HTTPException(status_code=400, detail="邮箱已存在")

    password_hash = auth.get_password_hash(req_data.password)

    user = await User.create(
        username=req_data.username, email=req_data.email, password_hash=password_hash
    )

    token = auth.create_access_token(data={"sub": str(user.id)})

    response_data = {"access_token": token, "token_type": "bearer", "user": user}
    return response_data


@router.post("/forgot-password")
async def sendResetEmail(data: ResetEmail):
    user = await User.filter(email=data.email)
    if not user:
        raise HTTPException(status_code=400, detail="邮箱没有被注册过")

    token = auth.create_access_token(data={"sub": data.email})
    url = f"http://localhost:8160/static/reset-password.html?token={token}"
    print(f"请打开链接重置密码：{url}")
    # return RedirectResponse(url=f"/static/reset-password.html?token={token}")

@router.post("/validate-reset-token", response_model=UserBase)
async def validateResetToken(data: VaildateResetToken):
    token = data.token
    payload = await auth.verify_token(token)
    if payload is None:
        raise HTTPException(status_code=400, detail="链接过期，请重新获取")
    email = payload.get("sub")
    user = await User.get_or_none(email=email)
    
    return user

@router.post("/reset-password")
async def ResetPassword(data: ResetPasswordSchemas):
    token = data.token
    payload = await auth.verify_token(token)
    if payload is None:
        raise HTTPException(status_code=400, detail="链接过期，请重新获取")
    email = payload.get("sub")
    user = await User.get_or_none(email=email)

    password_hash = auth.get_password_hash(data.new_password)
    user.password_hash = password_hash
    user = await user.save()

    return {"meg":"重置成功"}
    

