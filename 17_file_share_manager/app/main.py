from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, Response
from tortoise.contrib.starlette import register_tortoise
from api.routers import router
from database import TORTOISE_ORM
import os
from pathlib import Path


app = FastAPI(title="文件共享平台")

# 获取当前文件的绝对路径
BASE_DIR = Path(__file__).parent.parent
STATIC_DIR = BASE_DIR / "static"
UPLOAD_DIR = BASE_DIR / "uploads"

# 确保目录存在
STATIC_DIR.mkdir(exist_ok=True)
UPLOAD_DIR.mkdir(exist_ok=True)


app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

app.include_router(router, prefix="/api", tags=["api"])

register_tortoise(
    app,
    config=TORTOISE_ORM,
)


@app.get("/")
async def root():
    return RedirectResponse(url="/static/index.html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8170,
        reload=True,
        loop="asyncio",
    )
