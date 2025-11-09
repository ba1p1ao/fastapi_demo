from pydantic import BaseModel, field_validator
from typing import Optional
from fastapi import HTTPException
import re

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):

    password: str

    @field_validator("username")
    def username_valid(cls, value: str):
        value = value.replace("_", "")
        if not value.isalnum():
            raise HTTPException(
                status_code=400,
                detail="用户名存在特殊字符"
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
    
    @field_validator("password")
    def password_valid(cls, value):
        if len(value) < 6 or len(value) > 15:
            raise HTTPException(    
                status_code=400,
                detail="密码位数应该在6-15位之间"
            )
        return value
    
class UserLogin(BaseModel):
    username: str
    password: str



# 认证相关的模式
class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserBase



class ResetEmail(BaseModel):
    email: str

class VaildateResetToken(BaseModel):
    token: str

class ResetPasswordSchemas(VaildateResetToken):
    new_password: str