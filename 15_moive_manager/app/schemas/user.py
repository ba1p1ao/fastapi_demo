from datetime import datetime
from pydantic import BaseModel, field_validator
from typing import Optional
from fastapi import HTTPException
from models.user import User
import re


class UserBase(BaseModel):
    username: str
    email: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class UserCreate(UserBase):
    password: str

    @field_validator("email")
    def email_valid(cls, value):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, value):
            raise HTTPException(
            status_code=400,
            detail="邮箱不合法",
        )
        return value
    
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
    


class UserUpdate(UserBase):
    current_password:  Optional[str] = None
    new_password: Optional[str] = None

    @field_validator("current_password")
    def current_password_valid(cls, value):
        if not value:
            raise HTTPException(
                status_code=400,
                detail="当前密码不能为空"
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
    
class UserOut(UserBase):
    id: int
    avatar_url: Optional[str] = None
    created_at: datetime

class UserUpdatedOut(BaseModel):
    updatedUser: UserOut
    token: str
