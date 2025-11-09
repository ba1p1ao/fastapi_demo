from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from datetime import datetime
from apps import app01, app02, app03, app04, app05, app06, app07, app08

import asyncio  

app = FastAPI()
app.mount("/static", StaticFiles(directory="statics"))

app.include_router(app01.app01, prefix="/user", tags=["user test, 路径参数"])
app.include_router(app02.app02, prefix="/jobs", tags=["app02 test, 查询参数"])
app.include_router(app03.app03, prefix="/userinfo", tags=["app03 test, 数据校验"])
app.include_router(app04.app04, tags=["app04 test, form 表单数据"])
app.include_router(app05.app05, prefix="/file", tags=["app05 test, 文件上传"])
app.include_router(app06.app06, prefix="/request", tags=["app06 test, reqiest对象"])
app.include_router(app07.app07, prefix="/regiest", tags=["app07 test, 响应参数"])
app.include_router(app08.app08, prefix="/jinja2", tags=["app08 test, jinja2 模板"])

@app.get("/")
async def index():
    return "hello world"


# 健康检查端点
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "main",
        "timestamp": datetime.now().isoformat(),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8010,
        reload=True,
        # workers=2,  # 根据CPU核心数调整，避免过多worker竞争资源
        loop="asyncio",
        # limit_max_requests=1000,  # 处理1000个请求后重启worker，防止内存泄漏
        # timeout_keep_alive=5,  # 减少保持连接的时间
    )
