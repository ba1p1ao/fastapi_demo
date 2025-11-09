from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from routers import task
from backend.database import TORTOISE_ORM

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins="*",  # "*" 代表所有客户端
    allow_credentials=True,
    # allow_methods=["GET", "POST"], # ["GET", "POST"] 只允许 get post 请求
    allow_methods=["*"],
    allow_headers=["*"], 

)

register_tortoise(
    app=app,
    config=TORTOISE_ORM
)

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

app.include_router(task.task, prefix="/tasks", tags=["tasks router"])

@app.get("/")
async def index():
    return RedirectResponse(url="/frontend/index.html")




if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8100,
        loop="asyncio",
        reload=True
    )
