from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from database import TORTOISE_ORM
from api.routes import api_router

app = FastAPI(
    title="电商管理平台 API", description="电商管理平台后端API", version="1.0.0"
)
# 挂载静态文件（前端页面）
app.mount("/static", StaticFiles(directory="static"), name="static")
# CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中应该限制为具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# # 手动添加 CORS 头的中间件作为备用
# @app.middleware("http")
# async def add_cors_headers(request: Request, call_next):
#     response = await call_next(request)
    
#     # 确保响应头包含 CORS 信息
#     if "access-control-allow-origin" not in response.headers:
#         response.headers["Access-Control-Allow-Origin"] = "*"
#     if "access-control-allow-methods" not in response.headers:
#         response.headers["Access-Control-Allow-Methods"] = "*"
#     if "access-control-allow-headers" not in response.headers:
#         response.headers["Access-Control-Allow-Headers"] = "*"
#     if "access-control-allow-credentials" not in response.headers:
#         response.headers["Access-Control-Allow-Credentials"] = "true"
    
#     return response
# 数据库
register_tortoise(app, TORTOISE_ORM)

# 添加路由
app.include_router(api_router, prefix="/api", tags=["总路由"])


@app.get("/")
async def root():
    return RedirectResponse(url="/static/index.html")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "server": "0.0.0.0:8140"
    }

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8140,
        loop="asyncio",
        reload=True,
    )
