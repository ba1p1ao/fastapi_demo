from tortoise.models import Model

from tortoise import fields

# """
# CREATE TABLE movie_categories (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     movie_id INT,
#     category_id INT,
#     FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE,
#     FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
# );
# """

class MovieCategories(Model):
    # 注释: 电影与分类关联模型
    id = fields.IntField(pk=True)  # 主键
    movie = fields.ForeignKeyField(
        "models.Movie", related_name="movie_categories", on_delete=fields.CASCADE
    )  # 关联电影
    category = fields.ForeignKeyField(
        "models.Category", related_name="movie_categories", on_delete=fields.CASCADE
    )  # 关联分类

    class Meta:
        table = "movie_categories"

