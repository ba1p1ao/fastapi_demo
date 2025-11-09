from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from database import TORTOISE_ORM
from api.routers import api_router
app = FastAPI(title="电影网站")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/static/user_avatar_imgs", StaticFiles(directory="static/user_avatar_imgs"), name="user_avatar_imgs")

register_tortoise(
    app,
    config=TORTOISE_ORM,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, tags=["API"])

@app.get("/")
async def root():
    return RedirectResponse(url="/static/index.html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8150,
        reload=True,
    )
