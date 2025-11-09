from fastapi import APIRouter
from typing import Union, Optional

app02 = APIRouter()


# 查询参数
@app02.get("/")
async def get_jobs(kd, xl: Union[str, None] = None, gj: Optional[str]=None):
    # Union[str, None] = Optional[str]
    # 有默认参数即可以填也可以不填，没有默认参数是必须输入的
    # 基于kd，xl，gj数据库查询岗位信息
    return {
        "kd": kd,
        "xl": xl,
        "gj": gj,
    }


# 路径+查询参数
@app02.get("/{kd}")
async def get_jobs(kd, xl=None, gj=None):
    return {
        "kd": kd,
        "xl": xl,
        "gj": gj,
    }
