from tortoise.models import Model
from tortoise import fields
from datetime import datetime
from enum import Enum

# 分类枚举
class CategoryEnum(str, Enum):
    GAME = "game"
    TOOL = "tool"
    MOD = "mod"

# 权限枚举
class PermissionEnum(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"

# 游戏子分类枚举
class GameSubcategoryEnum(str, Enum):
    SHOOTER = "shooter"
    ACTION = "action"
    RPG = "rpg"
    STRATEGY = "strategy"
    SPORTS = "sports"
    RACING = "racing"
    SIMULATION = "simulation"

# 工具子分类枚举
class ToolSubcategoryEnum(str, Enum):
    CHEAT = "cheat"
    EDITOR = "editor"
    UTILITY = "utility"
    OPTIMIZATION = "optimization"

# 模组子分类枚举
class ModSubcategoryEnum(str, Enum):
    GRAPHICS = "graphics"
    GAMEPLAY = "gameplay"
    CONTENT = "content"
    UI = "ui"

# 用户表
class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True, description="用户名")
    email = fields.CharField(max_length=100, unique=True, description="邮箱")
    password_hash = fields.CharField(max_length=255, description="密码哈希")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")
    
    # 关联关系
    files = fields.ReverseRelation["File"]
    comments = fields.ReverseRelation["Comment"]
    likes = fields.ReverseRelation["Like"]
    collections = fields.ReverseRelation["Collection"]
    
    class Meta:
        table = "users"

# 文件表
class File(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="文件名")
    description = fields.TextField(description="文件描述")
    filename = fields.CharField(max_length=500, description="存储的文件名")
    file_path = fields.CharField(max_length=500, description="文件存储路径")
    file_size = fields.IntField(description="文件大小（字节）")
    
    # 分类字段
    category = fields.CharEnumField(CategoryEnum, description="文件分类")
    subcategory = fields.CharField(max_length=50, null=True, description="文件子分类")
    
    # 统计字段
    download_count = fields.IntField(default=0, description="下载次数")
    like_count = fields.IntField(default=0, description="点赞数")
    collect_count = fields.IntField(default=0, description="收藏数")
    
    # 权限设置
    permission = fields.CharEnumField(PermissionEnum, default=PermissionEnum.PUBLIC, description="文件权限")
    
    # 时间字段
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")
    
    # 外键关系
    author = fields.ForeignKeyField("models.User", related_name="uploaded_files", description="作者")
    
    # 关联关系
    comments = fields.ReverseRelation["Comment"]
    likes = fields.ReverseRelation["Like"]
    collections = fields.ReverseRelation["Collection"]
    shares = fields.ReverseRelation["Share"]
    
    class Meta:
        table = "files"
        indexes = [
            ("category", "subcategory"),  # 分类和子分类的复合索引
            ("download_count",),  # 下载量索引，用于热门排序
            ("created_at",),  # 创建时间索引，用于最新排序
        ]

# 评论表
class Comment(Model):
    id = fields.IntField(pk=True)
    content = fields.TextField(description="评论内容")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    
    # 外键关系
    user = fields.ForeignKeyField("models.User", related_name="user_comments", description="用户")
    file = fields.ForeignKeyField("models.File", related_name="file_comments", description="文件")
    
    class Meta:
        table = "comments"

# 点赞表
class Like(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    
    # 外键关系
    user = fields.ForeignKeyField("models.User", related_name="user_likes", description="用户")
    file = fields.ForeignKeyField("models.File", related_name="file_likes", description="文件")
    
    class Meta:
        table = "likes"
        unique_together = [("user", "file")]  # 防止重复点赞

# 收藏表
class Collection(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    
    # 外键关系
    user = fields.ForeignKeyField("models.User", related_name="user_collections", description="用户")
    file = fields.ForeignKeyField("models.File", related_name="file_collections", description="文件")
    
    class Meta:
        table = "collections"
        unique_together = [("user", "file")]  # 防止重复收藏

# 分享表
class Share(Model):
    id = fields.IntField(pk=True)
    share_token = fields.CharField(max_length=100, unique=True, description="分享令牌")
    share_link = fields.CharField(max_length=500, description="分享链接")
    password = fields.CharField(max_length=50, null=True, description="提取密码")
    expire_at = fields.DatetimeField(null=True, description="过期时间")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    
    # 外键关系
    file = fields.ForeignKeyField("models.File", related_name="file_shares", description="文件")
    
    class Meta:
        table = "shares"