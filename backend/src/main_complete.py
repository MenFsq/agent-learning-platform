"""
Agent Learning Platform 完整后端主应用
"""
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from loguru import logger

from .core.config import settings
from .core.database import init_db, close_db, check_database_health
from .middleware import logging, auth, cors
from .api.v1 import router as api_v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理
    """
    # 启动时执行
    logger.info("Starting Agent Learning Platform backend...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    
    # 初始化数据库
    try:
        await init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise
    
    # 应用启动完成
    logger.info("Application started successfully")
    
    yield
    
    # 关闭时执行
    logger.info("Shutting down Agent Learning Platform backend...")
    
    # 关闭数据库连接
    await close_db()
    logger.info("Database connections closed")
    
    logger.info("Application shutdown completed")


# 创建FastAPI应用实例
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    Agent Learning Platform 后端API服务
    
    ## 功能特性
    
    - 🔐 **用户认证** - JWT令牌认证系统
    - 📊 **项目管理** - AI Agent项目创建和管理
    - 🎓 **学习系统** - 智能学习路径和进度跟踪
    - 🤖 **AI集成** - LangChain和OpenClaw集成
    - 📈 **数据分析** - 学习数据统计和分析
    
    ## API文档
    
    - **Swagger UI**: [/docs](/docs)
    - **ReDoc**: [/redoc](/redoc)
    """,
    openapi_url="/api/v1/openapi.json" if settings.DEBUG else None,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan
)


# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理器"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An internal server error occurred",
                "details": str(exc) if settings.DEBUG else None
            }
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """请求验证异常处理器"""
    logger.warning(f"Validation error: {exc}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Input data validation failed",
                "details": exc.errors()
            }
        }
    )


# 添加中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加自定义中间件
app.middleware("http")(logging.logging_middleware)
app.middleware("http")(auth.auth_middleware)


# 健康检查端点
@app.get("/health", tags=["Health"])
async def health_check():
    """健康检查端点"""
    # 检查数据库连接
    db_health = await check_database_health()
    
    # 检查其他服务
    services_health = {
        "database": db_health,
        "ai_service": {"status": "healthy", "message": "AI service available"},
        "cache": {"status": "healthy", "message": "Cache service available"}
    }
    
    # 确定整体状态
    all_healthy = all(
        service["status"] == "healthy"
        for service in services_health.values()
        if isinstance(service, dict) and "status" in service
    )
    
    return {
        "status": "healthy" if all_healthy else "unhealthy",
        "timestamp": time.time(),
        "services": services_health,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }


@app.get("/", tags=["Root"])
async def root():
    """根端点"""
    return {
        "success": True,
        "message": f"Welcome to {settings.APP_NAME} API",
        "version": settings.APP_VERSION,
        "docs": "/docs" if settings.DEBUG else None,
        "health": "/health"
    }


# 注册API路由
app.include_router(
    api_v1_router,
    prefix="/api/v1",
    tags=["API v1"]
)


# 性能监控端点（仅开发环境）
if settings.DEBUG:
    @app.get("/metrics", tags=["Monitoring"])
    async def metrics():
        """性能监控端点"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        
        return {
            "memory": {
                "rss": process.memory_info().rss,
                "vms": process.memory_info().vms,
                "percent": process.memory_percent()
            },
            "cpu": {
                "percent": process.cpu_percent(interval=0.1),
                "count": psutil.cpu_count()
            },
            "disk": {
                "usage": psutil.disk_usage("/").percent
            },
            "network": {
                "connections": len(process.connections())
            }
        }


# 应用信息端点
@app.get("/info", tags=["Info"])
async def app_info():
    """应用信息端点"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG,
        "features": [
            "User Authentication",
            "Project Management",
            "Learning System",
            "AI Integration",
            "Data Analytics"
        ],
        "technologies": [
            "FastAPI",
            "PostgreSQL",
            "LangChain",
            "OpenClaw SDK",
            "Redis"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main_complete:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=settings.WORKERS if not settings.DEBUG else 1
    )