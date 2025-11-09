from fastapi import APIRouter, Request


app06 = APIRouter()


@app06.get("/")
async def get(request: Request):
    print(dict(request))
    return {
        "URL": request.url,
        "客户端IP地址:": request.client.host,   
        "客户端宿主": request.headers.get("user-agent"),
        "cookies": request.cookies,
    }