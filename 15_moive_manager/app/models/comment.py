from tortoise.models import Model
from tortoise import fields

# """
# CREATE TABLE comments (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     user_id INT,
#     movie_id INT,
#     content TEXT NOT NULL,
#     rating DECIMAL(2,1),
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
#     FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE
# );
# """

class Comment(Model):
    # 注释: 电影评论模型
    id = fields.IntField(pk=True)  # 主键
    user = fields.ForeignKeyField(
        "models.User", related_name="comments", on_delete=fields.CASCADE
    )  # 关联用户
    movie = fields.ForeignKeyField(
        "models.Movie", related_name="comments", on_delete=fields.CASCADE
    )  # 关联电影
    content = fields.TextField()  # 评论内容
    rating = fields.DecimalField(max_digits=2, decimal_places=1, null=True)  # 评分
    created_at = fields.DatetimeField(auto_now_add=True)  # 创建时间
    is_deleted = fields.BooleanField(default=False)  # 软删除标志
    deleted_at = fields.DatetimeField(null=True)  # 删除时间

    class Meta:
        table = "comments"

    
