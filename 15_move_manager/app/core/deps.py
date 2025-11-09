from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBasic, HTTPBearer
from tortoise.expressions import Q
from core import auth
from models.user import User
""""
工作原理
认证流程
客户端请求 → Bearer Token 验证 → 解析 Payload → 查询用户 → 返回用户对象
"""
# 创建 HTTP Bearer 认证方案实例
security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """获取当前用户依赖项"""
    # 从认证凭证中提取 JWT token
    token = credentials.credentials
    # 验证 token 的有效性
    payload = await auth.verify_token(token)
    if payload is None:
        # 如果 token 无效，抛出 400 错误
        raise HTTPException(
            status_code=400,
            detail="无效的认证令牌",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 从 token payload 中获取用户名 (JWT 标准中 'sub' 表示 subject)
    username: str = payload.get("sub")
    if username is None:
        # 如果 payload 中没有用户名，抛出 400 错误
        raise HTTPException(
            status_code=400,
            detail="无效的认证令牌",
        )

    # 从数据库中查询用户信息
    # print("token", username)
    user = await User.get_or_none(username=username)
    if user is None:
        # 如果用户不存在，抛出 400 错误
        raise HTTPException(
            status_code=400,
            detail="用户不存在",
        )
    # if not user.is_active:
    #     # 如果用户被禁用，抛出 400 错误
    #     raise HTTPException(
    #         status_code=400,
    #         detail="用户或密码错误",
    #     )
    # 返回用户对象，可以在路由处理函数中使用
    return user
