"""
安全认证和授权模块
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .config import settings

# 密码哈希上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Bearer认证
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """生成密码哈希"""
    return pwd_context.hash(password)


def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """创建访问令牌"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """创建刷新令牌"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
    
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_token(token: str) -> Dict[str, Any]:
    """解码JWT令牌"""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """获取当前用户依赖函数"""
    token = credentials.credentials
    payload = decode_token(token)
    
    # 检查令牌类型
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )
    
    # 检查用户ID是否存在
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    
    # 这里可以添加从数据库获取用户信息的逻辑
    # user = await user_service.get_user_by_id(user_id)
    # if not user or not user.is_active:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="User not found or inactive"
    #     )
    
    return payload


async def get_current_active_user(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """获取当前活跃用户"""
    # 这里可以添加用户状态检查逻辑
    # if not current_user.get("is_active", True):
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Inactive user"
    #     )
    return current_user


def validate_password_strength(password: str) -> bool:
    """验证密码强度"""
    if len(password) < 8:
        return False
    
    # 检查是否包含数字
    if not any(char.isdigit() for char in password):
        return False
    
    # 检查是否包含字母
    if not any(char.isalpha() for char in password):
        return False
    
    # 检查是否包含特殊字符
    special_characters = "!@#$%^&*()-_=+[]{}|;:,.<>?"
    if not any(char in special_characters for char in password):
        return False
    
    return True


def generate_api_key() -> str:
    """生成API密钥"""
    import secrets
    import string
    
    alphabet = string.ascii_letters + string.digits
    api_key = ''.join(secrets.choice(alphabet) for _ in range(32))
    return api_key


class RateLimiter:
    """API速率限制器"""
    
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests = {}
    
    async def check_limit(self, client_ip: str) -> bool:
        """检查是否超过速率限制"""
        import time
        
        current_time = time.time()
        minute_ago = current_time - 60
        
        # 清理过期的请求记录
        self.requests = {
            ip: [req_time for req_time in times if req_time > minute_ago]
            for ip, times in self.requests.items()
        }
        
        # 获取当前IP的请求记录
        client_requests = self.requests.get(client_ip, [])
        
        # 检查是否超过限制
        if len(client_requests) >= self.requests_per_minute:
            return False
        
        # 添加新的请求记录
        client_requests.append(current_time)
        self.requests[client_ip] = client_requests
        
        return True


# 创建默认的速率限制器
rate_limiter = RateLimiter()


# 安全中间件工具
class SecurityUtils:
    """安全工具类"""
    
    @staticmethod
    def sanitize_input(input_string: str) -> str:
        """清理用户输入，防止XSS攻击"""
        import html
        
        # HTML转义
        sanitized = html.escape(input_string)
        
        # 移除危险字符
        dangerous_chars = ["<script>", "</script>", "javascript:", "onload="]
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, "")
        
        return sanitized
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """验证邮箱格式"""
        import re
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def generate_csrf_token() -> str:
        """生成CSRF令牌"""
        import secrets
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def validate_csrf_token(token: str, stored_token: str) -> bool:
        """验证CSRF令牌"""
        return secrets.compare_digest(token, stored_token)


# 权限检查装饰器
def require_permission(permission: str):
    """权限检查装饰器"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # 这里可以实现具体的权限检查逻辑
            # current_user = kwargs.get("current_user")
            # if not has_permission(current_user, permission):
            #     raise HTTPException(
            #         status_code=status.HTTP_403_FORBIDDEN,
            #         detail="Insufficient permissions"
            #     )
            return await func(*args, **kwargs)
        return wrapper
    return decorator