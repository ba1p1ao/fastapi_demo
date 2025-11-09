from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

# JWT 配置
SECRET_KEY = "your-secret-key-here"  # 请在生产环境中更换为安全的密钥
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 密码哈希上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """生成密码哈希"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """创建 JWT token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def verify_token(token: str):
    """验证 JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
    



# """
# 我来详细解释这段JWT认证和密码哈希代码的每个部分。

# 导入的包及其作用
# 1. passlib.context
# python
# from passlib.context import CryptContext
# 作用：提供密码哈希和验证功能

# 原理：CryptContext 是一个密码哈希上下文管理器，支持多种哈希算法

# 特点：自动处理salt、迭代次数等安全参数

# 2. jose
# python
# from jose import JWTError, jwt
# 作用：JWT（JSON Web Token）的创建、编码、解码和验证

# jwt：主要的JWT操作模块

# JWTError：JWT验证失败时抛出的异常

# 3. datetime
# python
# from datetime import datetime, timedelta
# 作用：处理日期和时间，用于设置token过期时间

# datetime：表示具体的日期和时间点

# timedelta：表示时间间隔

# 4. typing
# python
# from typing import Optional
# 作用：提供类型提示，提高代码可读性

# Optional：表示参数可以是某种类型或None

# 配置常量
# python
# SECRET_KEY = "your-secret-key-here"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
# SECRET_KEY：用于签名JWT的密钥（生产环境必须使用强密钥）

# ALGORITHM：JWT签名算法，HS256使用对称加密

# ACCESS_TOKEN_EXPIRE_MINUTES：token默认有效期

# 密码哈希上下文
# python
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# schemes：指定使用的哈希算法（bcrypt是当前推荐的安全算法）

# deprecated：标记已弃用的算法，"auto"表示自动拒绝不安全的算法

# 函数详解
# 1. verify_password - 密码验证
# python
# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)
# 工作原理：

# 输入明文密码和数据库中存储的哈希值

# passlib自动提取哈希中的salt和算法参数

# 对明文密码使用相同参数进行哈希，然后比较结果

# 返回布尔值表示密码是否匹配

# 安全特性：

# 防止时序攻击

# 自动处理各种哈希格式

# 2. get_password_hash - 密码哈希
# python
# def get_password_hash(password: str) -> str:
#     return pwd_context.hash(password)
# 工作原理：

# 接收明文密码

# 自动生成随机的salt

# 使用bcrypt算法进行哈希

# 返回包含算法、salt和哈希值的字符串

# 输出示例：$2b$12$saltvalue.hashedpassword

# 3. create_access_token - 创建JWT
# python
# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#     to_encode = data.copy()  # 防止修改原始数据
#     if expires_delta:
#         expire = datetime.now() + expires_delta
#     else:
#         expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
#     to_encode.update({"exp": expire})  # 添加过期时间
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt
# JWT结构：

# Header：算法和类型（自动生成）

# Payload：传入的data + exp（过期时间）

# Signature：使用SECRET_KEY对前两部分签名

# 工作流程：

# 复制数据避免副作用

# 计算过期时间

# 添加exp字段到payload

# 使用HS256算法签名

# 4. verify_token - 验证JWT
# python
# async def verify_token(token: str):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         return payload
#     except JWTError:
#         return None
# 验证过程：

# 检查签名是否有效（防止篡改）

# 检查exp字段是否过期

# 检查其他标准声明（如iat、nbf等）

# 返回解码的payload或None

# 可能的JWTError：

# 签名验证失败

# token已过期

# token格式错误

# 算法不匹配

# 完整工作流程示例
# python
# # 用户注册
# password_hash = get_password_hash("user_password")
# # 存储 password_hash 到数据库

# # 用户登录
# if verify_password("input_password", password_hash):
#     # 密码正确，创建token
#     token = create_access_token({"sub": "user_id", "username": "john"})
    
# # 访问受保护资源
# payload = verify_token(token)
# if payload:
#     user_id = payload.get("sub")
#     # 允许访问
# 安全注意事项
# SECRET_KEY必须保持安全且足够复杂

# 生产环境使用环境变量存储密钥

# 考虑使用非对称算法（RS256）增强安全性

# 适当设置token过期时间平衡安全性和用户体验

# 使用HTTPS传输token防止中间人攻击

# 这套代码提供了完整的身份认证基础，可以集成到Web框架（如FastAPI、Django）中使用。

# """