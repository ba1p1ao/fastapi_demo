# 基于FastAPI and Mysql - 多用户局域网文件共享平台

![Python版本](https://img.shields.io/badge/Python-3.9+-brightgreen.svg "版本号")
![FastAPI版本](https://img.shields.io/badge/FastAPI-0.121+-ff69b4.svg "版本号")

## 简介
用于局域网内部文件共享服务

## 功能
- JWT token 认证。
- 使用 tortoise-orm (MySql).
- 文件上传与下载，用户管理自己的文件

### 项目结构
<details>
<summary>点击展开项目文件结构</summary>

```
├── app                         # 服务主目录
│   ├── api                     # API 文件夹
│   │   ├── endpoint            # endpoint 文件夹
│   │   │   ├── auth_user.py    # 用于用户认证（登录，注册）
│   │   │   ├── file.py         # 文件相关操作的API接口
│   │   │   └── user.py         # 用户相关操作的API接口
│   │   └── routers.py          # 总的路由文件
│   ├── config.py               # 配置文件
│   ├── core                    
│   │   ├── auth.py             # 用户 JWT 权限认证
│   │   ├── deps.py             # 用户 JWT 权限认证
│   ├── database.py             # 数据库配置文件
│   ├── main.py                 # 主项目入口
│   ├── migrations              # aerich 数据库迁移文件夹
│   ├── models      
│   │   ├── models.py           # tortoise models ORM模型文件
│   ├── pyproject.toml          # aerich 数据库迁移配置文件
│   └── schemas
│       ├── file.py             # 文件操作是数据pydantic校验文件
│       └── user.py             # 用户操作是数据pydantic校验文件
├── README.md
├── requirements.txt
├── static
│   └── index.html              # 前端文件
└── uploads                     # 文件物理总路径
```

</details>


## 如何使用

```
# 安装依赖库
pip install -r requirements.txt

# 建议使用 --upgrade 安装最新版 
pip install --upgrade -r requirements-dev.txt
```

## 配置你的数据库环境

参考 database.py 的配置信息设置数据库
或者 修改 database.py 内容与自己数据库匹配

## 迁移数据库

```
aerich init -t app/database.TORTOISE_ORM
aerich init-db
```


## 设置管理员用户

需要数据库操作
``` sql
-- 用户表数据
INSERT INTO users (username, password_hash, is_admin, created_at) VALUES
('admin', '$2b$12$LQv3c1yqBWVHxkd0L8k4CuB9g6ZYFgGZ8t8e4oA6p6WJkZ5J5J5Ju', 1, CURRENT_TIMESTAMP),
-- 注意：上面的密码哈希对应明文密码 "123123"

-- 文件表数据 - 根目录结构
INSERT INTO files (name, path, size, is_directory, mime_type, owner_id, parent_id, upload_time, modified_time) VALUES
('根目录', '/', 0, 1, NULL, 1, NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

```


## 运行启动

``` python
cd your_project/
uvicorn app/main:app --host="127.0.0.1" --port 8170

## 或者

cd your_project/
python app/main.py
```

## 访问页面

浏览器打开 http://localhost:8170/