from tortoise import fields, models
from tortoise.models import Model


class Users(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    password_hash = fields.CharField(max_length=255)
    is_admin = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    
    # 定义与 Files 的反向关系
    files: fields.ReverseRelation["Files"]
    
    def __str__(self):
        return self.username
    
    class Meta:
        table = "users"
        table_description = "用户表"


class Files(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    path = fields.CharField(max_length=1000)
    size = fields.IntField(default=0)
    is_directory = fields.BooleanField(default=False)
    mime_type = fields.CharField(max_length=100, null=True)
    
    # 外键关系
    owner: fields.ForeignKeyRelation[Users] = fields.ForeignKeyField(
        "models.Users", 
        related_name="files",
        on_delete=fields.CASCADE
    )
    parent: fields.ForeignKeyRelation["Files"] = fields.ForeignKeyField(
        "models.Files", 
        related_name="children",
        null=True,  # 允许根目录没有父级
        on_delete=fields.CASCADE
    )
    
    upload_time = fields.DatetimeField(auto_now_add=True)
    modified_time = fields.DatetimeField(auto_now=True)
    
    # 定义反向关系
    children: fields.ReverseRelation["Files"]
    
    def __str__(self):
        return self.name
    
    class Meta:
        table = "files"
        table_description = "文件表"
        indexes = [
            # ("path",),  # 为路径字段添加索引
            ("owner_id", "parent_id"),  # 复合索引
        ]