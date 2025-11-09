from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from core.config import TORTOISE_ORM
from routers import student
app = FastAPI()
app.include_router(student.student, prefix="/student", tags=["选课系统学生接口"])

# fastapi-旦运行，register_tortoise已经执行，实现监控
register_tortoise(
    app=app,
    config=TORTOISE_ORM
)
"""
`aerich init -t settings.TORTOISE_ORM` # 创建配置文件
    Success create migrate location ./migrations
    Success write config to pyproject.toml

`aerich init-db` # 创建数据库表
    Success create app migrate location migrations/models
    Success generate schema for app "models"
"""

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app", host="0.0.0.0", port=8030, reload=True, loop="asyncio"
    )
