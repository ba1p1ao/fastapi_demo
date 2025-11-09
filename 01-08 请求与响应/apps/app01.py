from fastapi import APIRouter

app01 = APIRouter()


# 路径参数
@app01.get("/{user_id}")
async def get_user(user_id):
    return {"user_name": f"{user_id}+user"}