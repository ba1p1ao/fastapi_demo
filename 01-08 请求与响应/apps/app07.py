from fastapi import APIRouter
from pydantic import BaseModel, field_validator, EmailStr, Field
from typing import Union, Optional, List
from hashlib import md5
import re

app07 = APIRouter()


class User(BaseModel):
    username: str
    password: str
    email: str
    full_name: Optional[str] = None

    @field_validator("email")
    def email_valid(cls, value):
        regex = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        assert re.fullmatch(regex, value), "电子邮件格式无效"
        return value

    # @field_validator("password")
    # def username_valid(cls, value):
    #     regex = re.compile(r'[a-zA-Z0-9_+-]')
    #     assert re.fullmatch(regex, value), "密码存在无效字符"
    #     return value


class UserOut(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: float = 10.5
    tags: List[str] = []


items = {
    "foo": {"name": "foo", "price": 12.2},
    "bar": {"name": "bar", "description": "bar description", "price": 20.2, "tax": 1},
    "baz": {
        "name": "baz",
        "description": "baz description",
        "price": 50.2,
        "tax": 1,
        "tag": ["sss", "bbb"],
    },
}


@app07.post("/user", response_model=UserOut)  # response_model 添加响应模型
async def create_user(user: User):
    # 存到数据库

    return user  # 返回的内容一定是 response_model “UserOut” 响应模型的序列化


@app07.get("/items", response_model=Item)
async def get_item(items_name: str):
    return items.get(items_name)


# # response_model_exclude_unset=True 排除为设置的值，只返回设置的值
# @app07.get("/items", response_model=Item, response_model_exclude_unset=True)
# async def get_item(items_name: str):
#     return items.get(items_name)


# # response_model_exclude_none 排除值为None的
# @app07.get("/items", response_model=Item, response_model_exclude_none=True)
# async def get_item(items_name: str):
#     return items.get(items_name)

# # response_model_exclude_defaults 排除值为默认的
# @app07.get("/items", response_model=Item, response_model_exclude_defaults=True)
# async def get_item(items_name: str):
#     return items.get(items_name)


# # response_model_exclude 返回的字段不包含 {} 里面的字段
# @app07.get("/items", response_model=Item, response_model_exclude={"description", "tax"})
# async def get_item(items_name: str):
#     return items.get(items_name)


# # response_model_include 返回的字段只包含 {} 里面的字段
# @app07.get("/items", response_model=Item, response_model_include={"description", "tax"})
# async def get_item(items_name: str):
#     return items.get(items_name)
