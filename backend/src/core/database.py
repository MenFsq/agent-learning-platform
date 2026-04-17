"""
数据库连接和初始化模块
"""
import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import text
from loguru import logger

from .config import settings, get_database_url

# 导入所有模型
from ..models.user import Base as UserBase
from ..models.project import Base as ProjectBase
from ..models.learning import Base as LearningBase
from ..models.system import Base as SystemBase

# 合并所有Base
Base = declarative_base()

database_url = get_database_url()
connect_args = {}
if database_url.startswith("postgresql+asyncpg://"):
    connect_args = {
        "timeout": 5,
        "command_timeout": 10,
    }

# 创建异步引擎
engine = create_async_engine(
    database_url,
    echo=settings.DEBUG,
    future=True,
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args=connect_args,
)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    获取数据库会话依赖
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """
    初始化数据库（创建所有表）
    """
    try:
        # 导入所有模型以确保它们被注册
        from ..models import user, project, learning, system
        
        async with engine.begin() as conn:
            # 创建所有表
            await conn.run_sync(Base.metadata.create_all)
            
            # 创建扩展（如果是PostgreSQL）
            if "postgresql" in get_database_url():
                await conn.execute(text("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\""))
            
            logger.info("Database tables created successfully")
            
            # 初始化默认数据
            await init_default_data(conn)
            
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise


async def init_default_data(conn):
    """
    初始化默认数据
    """
    try:
        # 检查是否已有系统设置
        from ..models.system import SystemSetting
        
        result = await conn.execute(
            text("SELECT COUNT(*) FROM system_settings WHERE key = 'system.initialized'")
        )
        count = result.scalar()
        
        if count == 0:
            # 插入默认系统设置
            default_settings = [
                {
                    "key": "system.initialized",
                    "value": True,
                    "data_type": "boolean",
                    "category": "system",
                    "description": "系统是否已初始化",
                    "is_public": False,
                    "is_editable": False,
                    "requires_admin": True
                },
                {
                    "key": "app.name",
                    "value": settings.APP_NAME,
                    "data_type": "string",
                    "category": "app",
                    "description": "应用名称",
                    "is_public": True,
                    "is_editable": True,
                    "requires_admin": True
                },
                {
                    "key": "app.version",
                    "value": settings.APP_VERSION,
                    "data_type": "string",
                    "category": "app",
                    "description": "应用版本",
                    "is_public": True,
                    "is_editable": False,
                    "requires_admin": True
                },
                {
                    "key": "user.registration.enabled",
                    "value": True,
                    "data_type": "boolean",
                    "category": "user",
                    "description": "是否允许用户注册",
                    "is_public": True,
                    "is_editable": True,
                    "requires_admin": True
                },
                {
                    "key": "user.default_role",
                    "value": "user",
                    "data_type": "string",
                    "category": "user",
                    "description": "新用户的默认角色",
                    "is_public": False,
                    "is_editable": True,
                    "requires_admin": True
                }
            ]
            
            for setting in default_settings:
                await conn.execute(
                    text("""
                    INSERT INTO system_settings 
                    (key, value, data_type, category, description, is_public, is_editable, requires_admin, created_at, updated_at)
                    VALUES (:key, :value, :data_type, :category, :description, :is_public, :is_editable, :requires_admin, NOW(), NOW())
                    """),
                    setting
                )
            
            logger.info("Default system settings initialized")
            
    except Exception as e:
        logger.warning(f"Failed to initialize default data: {e}")
        # 不抛出异常，因为表创建已经成功


async def check_database_health():
    """
    检查数据库连接健康状态
    """
    try:
        async with engine.connect() as conn:
            # 执行简单查询测试连接
            result = await conn.execute(text("SELECT 1"))
            result.scalar()
            
            # 检查表数量
            if "sqlite" in get_database_url():
                result = await conn.execute(
                    text("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
                )
            else:
                result = await conn.execute(
                    text("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public'")
                )
            
            table_count = result.scalar()
            
            return {
                "status": "healthy",
                "message": "Database connection successful",
                "tables": table_count,
                "type": "sqlite" if "sqlite" in get_database_url() else "postgresql"
            }
            
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {
            "status": "unhealthy",
            "message": str(e),
            "tables": 0,
            "type": "unknown"
        }


async def close_db():
    """
    关闭数据库连接
    """
    try:
        await engine.dispose()
        logger.info("Database connections closed")
    except Exception as e:
        logger.error(f"Error closing database connections: {e}")


async def reset_database():
    """
    重置数据库（删除所有表并重新创建）
    警告：仅用于开发和测试环境！
    """
    if settings.ENVIRONMENT not in ["development", "test"]:
        raise RuntimeError("Database reset is only allowed in development or test environment")
    
    try:
        async with engine.begin() as conn:
            # 删除所有表
            await conn.run_sync(Base.metadata.drop_all)
            logger.warning("All database tables dropped")
            
            # 重新创建所有表
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables recreated successfully")
            
            # 重新初始化默认数据
            await init_default_data(conn)
            
    except Exception as e:
        logger.error(f"Database reset failed: {e}")
        raise


# 导出所有模型
__all__ = [
    "get_db",
    "init_db",
    "close_db",
    "check_database_health",
    "reset_database",
    "Base",
    "AsyncSessionLocal",
    "engine",
]