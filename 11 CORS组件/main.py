from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# @app.middleware("http")
# async def corsmiddleware(request: Request, call_next):
#     response: Response = await call_next(request)
#     response.headers["Access-Control-Allow-Origin"] = "*"

#     return response
ORIGINS = [
    "http://192.168.10.106:8938"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",  # "*" 代表所有客户端
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"], 

)


@app.get("/user")
async def get():
    print("get user")
    return {"msg": "user"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8060, reload=True, loop="asyncio")
