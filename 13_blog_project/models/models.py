from tortoise.models import Model
from tortoise import fields


"""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100),
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""
class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True, null=False)
    email = fields.CharField(max_length=100, null=True)
    password_hash = fields.CharField(max_length=255, null=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "users"

    def __str__(self):
        return self.username

"""
-- 文章表 (更新)
CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    author_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES users (id) ON DELETE CASCADE
);
"""


class Post(Model):  # 改为单数形式，更符合命名规范
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255, null=False)
    content = fields.TextField(null=False)
    author = fields.ForeignKeyField("models.User", related_name="posts", on_delete=fields.CASCADE)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "posts"

    def __str__(self):
        return self.title