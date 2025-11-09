from fastapi import APIRouter
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import date

app03 = APIRouter()


class Addr(BaseModel):
    shenfen: str = ""
    chengshi: str = ""


class User(BaseModel):
    name: str
    age: int = Field(default=0, gt=0, lt=100)
    birth: Optional[date] = None
    friends: List[int] = []
    addr: Addr


    # 对 name 字段进行校验
    @field_validator("name")
    def name_must_alpha(cls, value: str):
        assert value.isalpha(), "name must be alpha"
        return value


class UserData(BaseModel):
    user_data: List[User]


@app03.post("/")
async def get_userinfo(user: User):
    return user


@app03.post("/data")
async def get_user_data(data: UserData):
    return data
