from fastapi import FastAPI, Request
from fastapi.responses import Response


app = FastAPI()


# 中间件的顺序是按照程序顺序加入栈里面，所以 request的顺序是 从下向上， response 是从上到下
#   中间件的顺序， 客户端 -> m1 request -> m2 request ->  服务器处理请求
#                  |   <- m1 response  <- m2 response <-|
#   request:    m1 , m2
#   response:   m2 , m1

# 中间件的修饰器，之后middleware， m1函数才是一个中间件函数，http 是协议
@app.middleware("http")
async def m2(request: Request, call_next):
    # 请求代码块
    print("m2 request")

    response: Response = await call_next(request)
    response.headers["auth"] = "cui"
    # 相应代码块
    print("m2 response")

    return response


@app.middleware("http")
async def m1(request: Request, call_next):
    # 请求代码块
    print("m1 request")
    # 添加黑名单，限制
    if request.client.host in ["192.168.10.106"] and request.url.path in ["/docs"]:
        return Response(status_code=403, content="<h1>403 fobidden</h1>")


    # if request.client.host in]
    response: Response = await call_next(request)

    # 相应代码块
    print("m1 response")

    return response


@app.get("/")
async def index():
    print("hello world")
    return "hello world"


@app.get("/user")
async def get():
    print("get user")
    return {"msg": "user"}


@app.get("/user/{user_id}")
async def get(user_id):
    print("get user_id")
    return {"msg": "user", "data": user_id}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8050, reload=True, loop="asyncio")
