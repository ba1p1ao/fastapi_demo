from fastapi import APIRouter, HTTPException
from models.models import Users
from schemas.user import UserCreate, Token
from core import auth
router = APIRouter()


@router.post("/login", response_model=Token)
async def login(data: UserCreate):
    print(data)
    user = await Users.get_or_none(username=data.username)
    if not user or not auth.verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    
    token = auth.create_access_token(data={"sub": str(user.id)})
    response_data = {
        "access_token" : token,
        "token_type": "bearer",
        "user": user
    }
    return response_data


@router.post("/register")
async def addUser(data: UserCreate):
    # print(data)
    user = await Users.get_or_none(username=data.username)
    if user:
        raise HTTPException(status_code=400, detail="用户已存在")
    
    password_hash = auth.get_password_hash(data.password)
    # print(password_hash)
    user = await Users.create(username=data.username, password_hash=password_hash)
    return {"msg", "success"}

