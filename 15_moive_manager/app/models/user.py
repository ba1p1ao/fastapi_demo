from tortoise.models import Model
from tortoise import fields


# """
# CREATE TABLE users (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     username VARCHAR(100) UNIQUE NOT NULL,
#     email VARCHAR(255) UNIQUE NOT NULL,
#     password_hash VARCHAR(255) NOT NULL,
#     avatar_url VARCHAR(500),
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );
# """


class User(Model):
    # 注释: 用户模型
    id = fields.IntField(pk=True)   # 主键
    username = fields.CharField(max_length=100, unique=True) # 用户名
    email = fields.CharField(max_length=255, unique=True) # 邮箱
    password_hash = fields.CharField(max_length=255) # 密码哈希
    avatar_url = fields.CharField(max_length=500, null=True) # 头像URL
    created_at = fields.DatetimeField(auto_now_add=True) # 创建时间

    class Meta:
        table = "users"


