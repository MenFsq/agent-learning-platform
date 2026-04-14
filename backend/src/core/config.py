"""
应用配置管理模块
"""
import os
from typing import List, Optional
from pydantic import AnyHttpUrl, PostgresDsn, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置类"""
    
    # 应用基础配置
    APP_NAME: str = "Agent Learning Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4
    
    # 数据库配置
    DATABASE_URL: str
    DATABASE_TEST_URL: Optional[str] = None
    
    # 安全配置
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS配置
    CORS_ORIGINS: List[AnyHttpUrl] = []
    
    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str] | str:
        """解析CORS origins配置"""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # AI服务配置
    OPENAI_API_KEY: Optional[str] = None
    OPENCLAW_API_KEY: Optional[str] = None
    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_ENDPOINT: Optional[str] = None
    LANGCHAIN_API_KEY: Optional[str] = None
    LANGCHAIN_PROJECT: str = "agent-learning-platform"
    
    # 缓存配置
    REDIS_URL: Optional[str] = None
    REDIS_CACHE_TTL: int = 3600
    
    # 文件存储配置
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    # 监控配置
    SENTRY_DSN: Optional[str] = None
    PROMETHEUS_PORT: int = 9090
    
    class Config:
        """Pydantic配置"""
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


# 创建全局配置实例
settings = Settings()


def get_database_url() -> str:
    """获取数据库URL，测试环境使用测试数据库"""
    if settings.ENVIRONMENT == "test" and settings.DATABASE_TEST_URL:
        return str(settings.DATABASE_TEST_URL)
    return str(settings.DATABASE_URL)


def is_development() -> bool:
    """判断是否为开发环境"""
    return settings.ENVIRONMENT == "development"


def is_testing() -> bool:
    """判断是否为测试环境"""
    return settings.ENVIRONMENT == "test"


def is_production() -> bool:
    """判断是否为生产环境"""
    return settings.ENVIRONMENT == "production"


# 创建必要的目录
def create_directories():
    """创建应用需要的目录"""
    directories = [
        settings.UPLOAD_DIR,
        "logs",
        "temp"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


# 应用启动时创建目录
create_directories()