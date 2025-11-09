from tortoise.models import Model
from tortoise import fields


# """
# CREATE TABLE categories (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(100) NOT NULL,
#     slug VARCHAR(100) UNIQUE
# );
# """


class Category(Model):
    # 注释: 电影分类模型
    id = fields.IntField(pk=True)   # 主键
    name = fields.CharField(max_length=100) # 分类名称
    slug = fields.CharField(max_length=100, unique=True) # 分类别名

    class Meta:
        table = "categories"
