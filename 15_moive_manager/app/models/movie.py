from tortoise.models import Model
from tortoise import fields


# """
# CREATE TABLE movies (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     title VARCHAR(255) NOT NULL,
#     cover_url VARCHAR(500),
#     description TEXT,
#     release_year INT,
#     duration INT, -- 分钟
#     rating DECIMAL(3,1),
#     director VARCHAR(255),
#     actors TEXT,
#     country VARCHAR(100),
#     language VARCHAR(100),
#     plot TEXT,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
# );
# """


class Movie(Model):
    # 注释: 电影模型
    id = fields.IntField(pk=True)   # 主键
    title = fields.CharField(max_length=255) # 电影标题
    cover_url = fields.CharField(max_length=500, null=True) # 封面图片URL
    description = fields.TextField(null=True) # 电影描述
    release_year = fields.IntField(null=True) # 上映年份
    duration = fields.IntField(null=True)  # 分钟
    rating = fields.DecimalField(max_digits=3, decimal_places=1, null=True) # 评分
    director = fields.CharField(max_length=255, null=True) # 导演
    actors = fields.TextField(null=True) #  主演
    country = fields.CharField(max_length=100, null=True) # 国家
    language = fields.CharField(max_length=100, null=True) # 语言
    plot = fields.TextField(null=True) # 剧情简介
    created_at = fields.DatetimeField(auto_now_add=True) # 创建时间
    updated_at = fields.DatetimeField(auto_now=True) # 更新时间

    class Meta:
        table = "movies"
