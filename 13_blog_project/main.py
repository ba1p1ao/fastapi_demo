from fastapi import FastAPI
from fastapi.responses import RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from core.database import TORTOISE_ORM
from routers import router_user, router_post

app = FastAPI()

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")
app.include_router(router_user.router_user, prefix="/api", tags=["router user"])
app.include_router(router_post.router_post, prefix="/api", tags=["router post"])
# 添加中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 链接数据库
register_tortoise(app=app, config=TORTOISE_ORM)


@app.get("/")
async def index():
    return RedirectResponse(url="/frontend/index.html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8070,
        loop="asyncio",
        reload=True,
    )
