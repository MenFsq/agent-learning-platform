"""
日志中间件模块
"""
import time
from typing import Callable
from fastapi import Request, Response
from loguru import logger


async def logging_middleware(request: Request, call_next: Callable) -> Response:
    """
    日志中间件
    
    记录所有HTTP请求的详细信息，包括：
    - 请求方法、路径、查询参数
    - 客户端IP地址
    - 请求处理时间
    - 响应状态码
    - 请求体大小（如果适用）
    """
    # 记录请求开始时间
    start_time = time.time()
    
    # 获取客户端IP
    client_ip = request.client.host if request.client else "unknown"
    
    # 获取请求路径和查询参数
    path = request.url.path
    query_params = str(request.query_params) if request.query_params else ""
    
    # 记录请求信息
    logger.info(
        f"Request started: {request.method} {path}"
        f"{'?' + query_params if query_params else ''} "
        f"from {client_ip}"
    )
    
    try:
        # 处理请求
        response = await call_next(request)
        
        # 计算处理时间
        process_time = time.time() - start_time
        
        # 记录响应信息
        logger.info(
            f"Request completed: {request.method} {path} "
            f"status={response.status_code} "
            f"time={process_time:.3f}s"
        )
        
        # 添加处理时间到响应头
        response.headers["X-Process-Time"] = str(process_time)
        
        return response
        
    except Exception as e:
        # 记录异常信息
        process_time = time.time() - start_time
        logger.error(
            f"Request failed: {request.method} {path} "
            f"error={str(e)} "
            f"time={process_time:.3f}s"
        )
        raise


class RequestLogger:
    """请求日志记录器"""
    
    @staticmethod
    async def log_request_details(request: Request):
        """记录请求详细信息"""
        try:
            # 获取请求体（对于非GET请求）
            if request.method in ["POST", "PUT", "PATCH"]:
                body = await request.body()
                if body:
                    logger.debug(f"Request body: {body[:500]}...")  # 限制日志长度
        except Exception as e:
            logger.warning(f"Failed to read request body: {e}")
    
    @staticmethod
    def log_response_details(response: Response):
        """记录响应详细信息"""
        # 记录响应头
        logger.debug(f"Response headers: {dict(response.headers)}")
        
        # 记录响应体大小
        content_length = response.headers.get("content-length")
        if content_length:
            logger.debug(f"Response size: {content_length} bytes")


# 结构化日志配置
def setup_logging():
    """配置结构化日志"""
    import sys
    from loguru import logger
    
    # 移除默认的处理器
    logger.remove()
    
    # 控制台输出（开发环境）
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
               "<level>{message}</level>",
        level="DEBUG" if settings.DEBUG else "INFO",
        colorize=True
    )
    
    # 文件输出（生产环境）
    logger.add(
        settings.LOG_FILE,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        level=settings.LOG_LEVEL,
        rotation="10 MB",  # 日志文件轮转：10MB
        retention="30 days",  # 保留30天
        compression="zip"  # 压缩旧日志
    )
    
    # 错误日志单独文件
    logger.add(
        "logs/error.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        level="ERROR",
        rotation="10 MB",
        retention="90 days"
    )
    
    return logger


# 性能监控日志
class PerformanceLogger:
    """性能监控日志记录器"""
    
    @staticmethod
    def log_slow_request(request: Request, process_time: float, threshold: float = 1.0):
        """记录慢请求"""
        if process_time > threshold:
            logger.warning(
                f"Slow request detected: {request.method} {request.url.path} "
                f"time={process_time:.3f}s (threshold={threshold}s)"
            )
    
    @staticmethod
    def log_database_query(query: str, execution_time: float, threshold: float = 0.1):
        """记录慢数据库查询"""
        if execution_time > threshold:
            logger.warning(
                f"Slow database query: {query[:100]}... "
                f"time={execution_time:.3f}s (threshold={threshold}s)"
            )
    
    @staticmethod
    def log_external_api_call(url: str, method: str, execution_time: float, threshold: float = 2.0):
        """记录外部API调用"""
        if execution_time > threshold:
            logger.warning(
                f"Slow external API call: {method} {url} "
                f"time={execution_time:.3f}s (threshold={threshold}s)"
            )


# 审计日志
class AuditLogger:
    """审计日志记录器"""
    
    @staticmethod
    def log_user_action(user_id: str, action: str, resource: str, details: dict = None):
        """记录用户操作"""
        logger.info(
            f"User action: user={user_id} action={action} resource={resource} "
            f"details={details or {}}"
        )
    
    @staticmethod
    def log_security_event(event_type: str, severity: str, details: dict):
        """记录安全事件"""
        logger.warning(
            f"Security event: type={event_type} severity={severity} details={details}"
        )
    
    @staticmethod
    def log_data_change(
        user_id: str,
        operation: str,
        table: str,
        record_id: str,
        old_data: dict = None,
        new_data: dict = None
    ):
        """记录数据变更"""
        logger.info(
            f"Data change: user={user_id} operation={operation} table={table} "
            f"record={record_id} old={old_data} new={new_data}"
        )


# 业务日志
class BusinessLogger:
    """业务日志记录器"""
    
    @staticmethod
    def log_project_creation(project_id: str, user_id: str, project_name: str):
        """记录项目创建"""
        logger.info(
            f"Project created: id={project_id} user={user_id} name={project_name}"
        )
    
    @staticmethod
    def log_learning_progress(user_id: str, module_id: str, progress: int):
        """记录学习进度"""
        logger.info(
            f"Learning progress: user={user_id} module={module_id} progress={progress}%"
        )
    
    @staticmethod
    def log_ai_interaction(
        user_id: str,
        interaction_type: str,
        input_data: dict,
        output_data: dict,
        duration: float
    ):
        """记录AI交互"""
        logger.info(
            f"AI interaction: user={user_id} type={interaction_type} "
            f"duration={duration:.3f}s input={input_data} output={output_data}"
        )


# 导入配置
from ..core.config import settings

# 初始化日志配置
logger = setup_logging()