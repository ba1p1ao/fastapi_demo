from fastapi import HTTPException, status
from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional, List
import re


class UserBase(BaseModel):
    username: str
    email: Optional[str] = None


class UserCreate(UserBase):
    password: str

    @field_validator("username")
    def username_valid(cls, value):
        if not value.isalnum():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名存在特殊字符",
            )

        return value

    @field_validator("password")
    def password_valid(cls, value):
        if len(value) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="密码必须大于6位",
            )
        return value

    @field_validator("email")
    def email_valid(cls, value):
        if value:
            pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
            if not re.match(pattern, value):
                raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱不合法",
            )
        return value


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None

    @field_validator("username")
    def username_valid(cls, value):
        if not value.isalnum():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名存在特殊字符",
            )

        return value

    @field_validator("email")
    def email_valid(cls, value):
        if value:
            pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
            if not re.match(pattern, value):
                raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="email 不合法",
            )
        return value


# 认证相关的模式
class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class TokenData(BaseModel):
    username: Optional[str] = None
