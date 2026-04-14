"""
用户数据模式
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, validator, Field
from enum import Enum


class UserRole(str, Enum):
    """用户角色枚举"""
    ADMIN = "admin"
    USER = "user"
    DEVELOPER = "developer"
    MANAGER = "manager"


# 基础模型
class UserBase(BaseModel):
    """用户基础模型"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=200)
    
    @validator('username')
    def validate_username(cls, v):
        if not v.isalnum() and '_' not in v:
            raise ValueError('Username can only contain letters, numbers, and underscores')
        return v


# 创建模型
class UserCreate(UserBase):
    """用户创建模型"""
    password: str = Field(..., min_length=8)
    confirm_password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        # 检查密码复杂度
        has_letter = any(c.isalpha() for c in v)
        has_digit = any(c.isdigit() for c in v)
        if not (has_letter and has_digit):
            raise ValueError('Password must contain both letters and numbers')
        return v
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v


# 更新模型
class UserUpdate(BaseModel):
    """用户更新模型"""
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=200)
    password: Optional[str] = Field(None, min_length=8)
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    
    @validator('password')
    def validate_password(cls, v):
        if v is not None and len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v
    
    @validator('username')
    def validate_username(cls, v):
        if v is not None and not v.isalnum() and '_' not in v:
            raise ValueError('Username can only contain letters, numbers, and underscores')
        return v


# 个人资料更新模型
class UserProfileUpdate(BaseModel):
    """用户个人资料更新模型"""
    full_name: Optional[str] = Field(None, max_length=200)
    avatar_url: Optional[str] = None
    bio: Optional[str] = None


# 登录模型
class UserLogin(BaseModel):
    """用户登录模型"""
    username: str  # 可以是用户名或邮箱
    password: str


# 响应模型
class UserResponse(UserBase):
    """用户响应模型"""
    id: int
    avatar_url: Optional[str]
    bio: Optional[str]
    role: UserRole
    is_active: bool
    is_verified: bool
    last_login: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# 简化的用户响应
class UserSimpleResponse(BaseModel):
    """简化用户响应模型"""
    id: int
    username: str
    email: EmailStr
    full_name: Optional[str]
    avatar_url: Optional[str]
    role: UserRole
    
    class Config:
        from_attributes = True


# 令牌响应
class TokenResponse(BaseModel):
    """令牌响应模型"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: Optional[int] = 3600


# 刷新令牌请求
class TokenRefreshRequest(BaseModel):
    """刷新令牌请求模型"""
    refresh_token: str


# 密码重置请求
class PasswordResetRequest(BaseModel):
    """密码重置请求模型"""
    email: EmailStr


# 密码重置确认
class PasswordResetConfirm(BaseModel):
    """密码重置确认模型"""
    token: str
    new_password: str = Field(..., min_length=8)
    confirm_password: str
    
    @validator('new_password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        has_letter = any(c.isalpha() for c in v)
        has_digit = any(c.isdigit() for c in v)
        if not (has_letter and has_digit):
            raise ValueError('Password must contain both letters and numbers')
        return v
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v


# 用户列表响应
class UserListResponse(BaseModel):
    """用户列表响应模型"""
    total: int
    users: List[UserResponse]
    page: int
    page_size: int
    total_pages: int


# 用户统计
class UserStats(BaseModel):
    """用户统计模型"""
    total_users: int
    active_users: int
    verified_users: int
    users_by_role: dict
    new_users_today: int
    new_users_this_week: int
    new_users_this_month: int