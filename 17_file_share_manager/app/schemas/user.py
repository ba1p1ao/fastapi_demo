from datetime import datetime
from pydantic import BaseModel, field_validator
from fastapi import HTTPException


class UserCreate(BaseModel):
    username: str
    password: str

    @field_validator("username")
    def username_valid(cls, v: str):
        v = v.replace("_", "")
        if not v.isalnum():
            raise HTTPException(status_code=400, detail="用户名包含特殊符号")

        return v

    @field_validator("password")
    def password_valid(cls, v: str):
        if len(v) < 6:
            raise HTTPException(status_code=400, detail="密码不能少于6位")

        return v


class UserResponse(BaseModel):
    id: int
    username: str
    created_at: datetime
    is_admin: bool = False

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse