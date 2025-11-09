import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "电商管理平台"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # JWT配置（如果后续需要认证）
    SECRET_KEY: str = os.getenv("SECRET_KEY", "cuishiyuan")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()