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
                "database": "task_manager",
                "minsize": 1,
                "maxsize": 5,
                "charset": "utf8mb4",
                "echo": True,
            },
        }
    },
    "apps": {
        "models": {
            # 执行 aerich init-db models 相当于是包路径相对路径是与 pyproject.toml 为同一级
            # "aerich.models" 自己的模型类，必须加
            "models": ["backend.models", "aerich.models"],
            "default_connection": "default",
        }
    },
    "use_tz": False,
    "timezone": "Asia/Shanghai",
}
