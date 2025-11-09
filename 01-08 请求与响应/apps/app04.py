# form 表单数据

from fastapi import APIRouter, Form


app04 = APIRouter()

@app04.post("/regit")
async def regist(username: str = Form(), password: str = Form()):
    return {
        "username": username, 
        "password": password
    }
