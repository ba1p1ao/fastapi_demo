from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from database import TORTOISE_ORM
from api.routers import api_router


app = FastAPI(title="游戏文件网站")
# CORS 中间件配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 连接数据库
register_tortoise(
    app, config=TORTOISE_ORM
)
# 静态文件配置
app.mount("/static", StaticFiles(directory="static"), name="static")

# 添加路由
app.include_router(api_router, prefix="/api", tags=["api"])


@app.get("/")
async def index():
    return RedirectResponse(url="/static/index.html")



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8160,
        reload=True,
        loop="asyncio",
    )