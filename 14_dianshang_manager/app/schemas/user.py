from fastapi import HTTPException
from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional
import re

class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str

    @field_validator("username")
    def username_valid(cls, value: str):
        if not value.isalnum():
            raise HTTPException(
                status_code=400,
                detail="用户名存在特殊字符"
            )
        return value
    

    @field_validator("password")
    def password_valid(cls, value):
        if len(value) < 6 or len(value) > 15:
            raise HTTPException(
                status_code=400,
                detail="密码位数应该在6-15位之间"
            )
        return value
    
    @field_validator("email")
    def email_valid(cls, value):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, value):
            raise HTTPException(
            status_code=400,
            detail="邮箱不合法",
        )
        return value
    

class UserLogin(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    email: Optional[str] = None
    new_password: Optional[str] = None
    old_password: Optional[str] = None

    @field_validator("email")
    def email_valid(cls, value):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, value):
            raise HTTPException(
            status_code=400,
            detail="邮箱不合法",
        )
        return value
    
    @field_validator("new_password")
    def password_valid(cls, value):
        if len(value) < 6 or len(value) > 15:
            raise HTTPException(
                status_code=400,
                detail="密码位数应该在6-15位之间"
            )
        return value
    
class UserResponse(UserBase):
    id: int
    created_at: datetime
    is_active: bool

# 认证相关的模式
class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

