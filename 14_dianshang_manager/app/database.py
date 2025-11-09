# tortoise_orm config 配置参数
TORTOISE_ORM = {
    "connections": {
        "default": {
            #'engine':'tortoise.backends.asyncpg',PostgreSQL
            "engine": "tortoise.backends.mysql",  # MySQL or Mariadb
            "credentials": {
                "host": "127.0.0.1",
                "port": "3307",
                "user": "root",
                "password": "123",
                "database": "dianshang_manager",
                "minsize": 1,
                "maxsize": 5,
                "charset": "utf8mb4",
                "echo": True,
            },
        }
    },
    "apps": {
        "models": {
            "models": [
                "models.user", 
                "models.product",
                "models.order",
                "models.order_item",
                "aerich.models"
                ], # "aerich.models" 自己的模型类，必须加
            "default_connection": "default",
        }
    },
    "use_tz": False,
    "timezone": "Asia/Shanghai",
}
