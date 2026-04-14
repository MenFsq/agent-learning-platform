"""
认证和授权中间件
"""
from typing import Callable, Optional
from fastapi import Request, Response, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

from ..core.config import settings
from ..core.security import decode_token
from ..middleware.logging import logger


async def auth_middleware(request: Request, call_next: Callable) -> Response:
    """
    认证中间件
    
    处理JWT令牌验证和用户认证
    """
    # 定义不需要认证的路径
    public_paths = [
        "/",
        "/health",
        "/info",
        "/docs",
        "/redoc",
        "/openapi.json",
        "/api/v1/auth/login",
        "/api/v1/auth/register",
        "/api/v1/auth/refresh",
        "/api/v1/auth/verify-email"
    ]
    
    # 检查是否为公开路径
    if request.url.path in public_paths or request.url.path.startswith("/static/"):
        return await call_next(request)
    
    # 获取授权头
    auth_header = request.headers.get("Authorization")
    
    if not auth_header:
        logger.warning(f"Missing authorization header for path: {request.url.path}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 验证授权头格式
    if not auth_header.startswith("Bearer "):
        logger.warning(f"Invalid authorization header format: {auth_header}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 提取令牌
    token = auth_header[7:]  # 移除"Bearer "前缀
    
    try:
        # 解码和验证令牌
        payload = decode_token(token)
        
        # 检查令牌类型
        token_type = payload.get("type")
        if token_type != "access":
            logger.warning(f"Invalid token type: {token_type}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        
        # 将用户信息添加到请求状态
        request.state.user = payload
        
        # 记录认证成功
        user_id = payload.get("sub", "unknown")
        logger.info(f"User authenticated: id={user_id} path={request.url.path}")
        
    except JWTError as e:
        logger.warning(f"JWT validation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in auth middleware: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    
    # 继续处理请求
    return await call_next(request)


class RoleBasedAuth:
    """基于角色的认证"""
    
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles
    
    async def __call__(self, request: Request):
        """检查用户角色"""
        user = getattr(request.state, "user", None)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated"
            )
        
        user_role = user.get("role", "user")
        
        if user_role not in self.allowed_roles:
            logger.warning(
                f"Permission denied: user={user.get('sub')} "
                f"role={user_role} allowed={self.allowed_roles}"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        
        return user


class PermissionBasedAuth:
    """基于权限的认证"""
    
    def __init__(self, required_permission: str):
        self.required_permission = required_permission
    
    async def __call__(self, request: Request):
        """检查用户权限"""
        user = getattr(request.state, "user", None)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated"
            )
        
        user_permissions = user.get("permissions", [])
        
        if self.required_permission not in user_permissions:
            logger.warning(
                f"Permission denied: user={user.get('sub')} "
                f"required={self.required_permission} "
                f"has={user_permissions}"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        
        return user


class RateLimitMiddleware:
    """速率限制中间件"""
    
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests = {}
    
    async def __call__(self, request: Request, call_next: Callable) -> Response:
        """应用速率限制"""
        # 获取客户端标识
        client_ip = request.client.host if request.client else "unknown"
        user_id = getattr(request.state, "user", {}).get("sub", "anonymous")
        client_id = f"{client_ip}:{user_id}"
        
        import time
        
        current_time = time.time()
        minute_ago = current_time - 60
        
        # 清理过期的请求记录
        self.requests = {
            cid: [req_time for req_time in times if req_time > minute_ago]
            for cid, times in self.requests.items()
        }
        
        # 获取当前客户端的请求记录
        client_requests = self.requests.get(client_id, [])
        
        # 检查是否超过限制
        if len(client_requests) >= self.requests_per_minute:
            logger.warning(
                f"Rate limit exceeded: client={client_id} "
                f"requests={len(client_requests)} limit={self.requests_per_minute}"
            )
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded",
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(int(minute_ago + 60))
                }
            )
        
        # 添加新的请求记录
        client_requests.append(current_time)
        self.requests[client_id] = client_requests
        
        # 添加速率限制头
        response = await call_next(request)
        
        remaining = self.requests_per_minute - len(client_requests)
        reset_time = int(minute_ago + 60)
        
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(reset_time)
        
        return response


class CSRFProtectionMiddleware:
    """CSRF保护中间件"""
    
    async def __call__(self, request: Request, call_next: Callable) -> Response:
        """应用CSRF保护"""
        # 只对修改数据的请求进行CSRF检查
        if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            # 检查CSRF令牌
            csrf_token = request.headers.get("X-CSRF-Token")
            cookie_token = request.cookies.get("csrf_token")
            
            if not csrf_token or not cookie_token:
                logger.warning("Missing CSRF tokens")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="CSRF token missing"
                )
            
            if csrf_token != cookie_token:
                logger.warning("CSRF token mismatch")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="CSRF token invalid"
                )
        
        return await call_next(request)


class APIKeyMiddleware:
    """API密钥认证中间件"""
    
    async def __call__(self, request: Request, call_next: Callable) -> Response:
        """验证API密钥"""
        # 检查API密钥头
        api_key = request.headers.get("X-API-Key")
        
        if not api_key:
            # 如果没有API密钥，使用常规的JWT认证
            return await call_next(request)
        
        # 验证API密钥
        # 这里应该从数据库或配置中验证API密钥
        # valid_api_keys = await get_valid_api_keys()
        
        # if api_key not in valid_api_keys:
        #     logger.warning(f"Invalid API key: {api_key[:10]}...")
        #     raise HTTPException(
        #         status_code=status.HTTP_401_UNAUTHORIZED,
        #         detail="Invalid API key"
        #     )
        
        # 记录API密钥使用
        logger.info(f"API key used: {api_key[:10]}... for path: {request.url.path}")
        
        # 继续处理请求
        return await call_next(request)


# 创建中间件实例
rate_limit_middleware = RateLimitMiddleware()
csrf_protection_middleware = CSRFProtectionMiddleware()
api_key_middleware = APIKeyMiddleware()


# 工具函数
def get_current_user(request: Request) -> Optional[dict]:
    """从请求中获取当前用户"""
    return getattr(request.state, "user", None)


def require_authentication(request: Request) -> dict:
    """要求认证，如果未认证则抛出异常"""
    user = get_current_user(request)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    return user


def get_user_id(request: Request) -> Optional[str]:
    """获取用户ID"""
    user = get_current_user(request)
    return user.get("sub") if user else None


def get_user_role(request: Request) -> Optional[str]:
    """获取用户角色"""
    user = get_current_user(request)
    return user.get("role") if user else None


def has_permission(request: Request, permission: str) -> bool:
    """检查用户是否有特定权限"""
    user = get_current_user(request)
    if not user:
        return False
    
    user_permissions = user.get("permissions", [])
    return permission in user_permissions


def has_role(request: Request, role: str) -> bool:
    """检查用户是否有特定角色"""
    user_role = get_user_role(request)
    return user_role == role if user_role else False