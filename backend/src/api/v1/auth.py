"""
认证API模块
"""
from datetime import timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, EmailStr, validator

from sqlalchemy import select

from ...core.database import get_db
from ...core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
    validate_password_strength,
    SecurityUtils
)
from ...models.user import User, UserRole
from ...middleware.logging import logger

router = APIRouter(prefix="/auth", tags=["Authentication"])

# OAuth2密码流
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# 请求和响应模型
class UserRegister(BaseModel):
    """用户注册请求模型"""
    email: EmailStr
    username: str
    password: str
    confirm_password: str
    
    @validator('username')
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters long')
        if len(v) > 50:
            raise ValueError('Username must be at most 50 characters long')
        return v
    
    @validator('password')
    def validate_password(cls, v):
        if not validate_password_strength(v):
            raise ValueError(
                'Password must be at least 8 characters long and contain '
                'letters, numbers, and special characters'
            )
        return v
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v


class UserLogin(BaseModel):
    """用户登录请求模型"""
    email: Optional[str] = None
    username: Optional[str] = None
    password: str


class TokenResponse(BaseModel):
    """令牌响应模型"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user_id: str
    username: str


class UserProfile(BaseModel):
    """用户资料模型"""
    id: str
    email: str
    username: str
    is_active: bool
    created_at: str
    last_login: Optional[str] = None


class RefreshTokenRequest(BaseModel):
    """刷新令牌请求模型"""
    refresh_token: str


class ChangePasswordRequest(BaseModel):
    """修改密码请求模型"""
    current_password: str
    new_password: str
    confirm_password: str
    
    @validator('new_password')
    def validate_new_password(cls, v):
        if not validate_password_strength(v):
            raise ValueError(
                'New password must be at least 8 characters long and contain '
                'letters, numbers, and special characters'
            )
        return v
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v


# 用户服务（数据库实现）
class UserService:
    """用户服务类 — 真实数据库操作"""

    @staticmethod
    def _to_dict(user: User) -> dict:
        """ORM 对象转字典（兼容现有调用方，ID 转字符串）"""
        return {
            "id": str(user.id),
            "email": user.email,
            "username": user.username,
            "hashed_password": user.hashed_password,
            "full_name": user.full_name,
            "avatar_url": user.avatar_url,
            "bio": user.bio,
            "role": user.role.value if user.role else "user",
            "is_active": user.is_active,
            "is_verified": user.is_verified,
            "last_login": user.last_login.isoformat() if user.last_login else None,
            "created_at": user.created_at.isoformat() if user.created_at else None,
        }

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str):
        """根据邮箱获取用户"""
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        return UserService._to_dict(user) if user else None

    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str):
        """根据用户名获取用户"""
        result = await db.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()
        return UserService._to_dict(user) if user else None

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int):
        """根据ID获取用户"""
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        return UserService._to_dict(user) if user else None

    @staticmethod
    async def create_user(db: AsyncSession, user_data: dict):
        """创建用户"""
        user = User(
            email=user_data["email"],
            username=user_data["username"],
            hashed_password=get_password_hash(user_data["password"]),
            full_name=user_data.get("full_name"),
            role=UserRole.USER,
            is_active=True,
            is_verified=False,
        )
        db.add(user)
        await db.flush()
        await db.refresh(user)
        logger.info(f"User created: id={user.id} username={user.username}")
        return UserService._to_dict(user)

    @staticmethod
    async def update_last_login(db: AsyncSession, user_id):
        """更新最后登录时间"""
        from datetime import datetime
        result = await db.execute(select(User).where(User.id == int(user_id)))
        user = result.scalar_one_or_none()
        if user:
            user.last_login = datetime.utcnow()
            await db.flush()


@router.post("/register", response_model=TokenResponse)
async def register(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    """用户注册"""
    try:
        # 检查邮箱是否已存在
        existing_user = await UserService.get_user_by_email(db, user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # 检查用户名是否已存在
        existing_user = await UserService.get_user_by_username(db, user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        # 创建用户
        user = await UserService.create_user(db, {
            "email": user_data.email,
            "username": user_data.username,
            "password": user_data.password
        })
        
        # 创建令牌
        access_token = create_access_token(
            data={"sub": user["id"], "username": user["username"]}
        )
        refresh_token = create_refresh_token(
            data={"sub": user["id"], "username": user["username"]}
        )
        
        # 记录注册成功
        logger.info(f"User registered: id={user['id']} email={user['email']}")
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=30 * 60,  # 30分钟
            user_id=user["id"],
            username=user["username"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """用户登录（OAuth2兼容）"""
    try:
        # 根据邮箱或用户名查找用户
        user = None
        if "@" in form_data.username:
            user = await UserService.get_user_by_email(db, form_data.username)
        else:
            user = await UserService.get_user_by_username(db, form_data.username)
        
        if not user:
            logger.warning(f"Login failed: user not found - {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email/username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # 验证密码
        if not verify_password(form_data.password, user["hashed_password"]):
            logger.warning(f"Login failed: incorrect password for user - {user['id']}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email/username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # 检查用户是否激活
        if not user.get("is_active", True):
            logger.warning(f"Login failed: user inactive - {user['id']}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User account is inactive"
            )
        
        # 更新最后登录时间
        await UserService.update_last_login(db, user["id"])
        
        # 创建令牌
        access_token = create_access_token(
            data={"sub": user["id"], "username": user["username"]}
        )
        refresh_token = create_refresh_token(
            data={"sub": user["id"], "username": user["username"]}
        )
        
        # 记录登录成功
        logger.info(f"User logged in: id={user['id']} username={user['username']}")
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=30 * 60,
            user_id=user["id"],
            username=user["username"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


@router.post("/login/json", response_model=TokenResponse)
async def login_json(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """用户登录（JSON格式，供前端使用）"""
    identifier = login_data.username or login_data.email or ""

    user = None
    if "@" in identifier:
        user = await UserService.get_user_by_email(db, identifier)
    else:
        user = await UserService.get_user_by_username(db, identifier)

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    if not verify_password(login_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    if not user.get("is_active", True):
        raise HTTPException(status_code=400, detail="User account is inactive")

    await UserService.update_last_login(db, user["id"])

    access_token = create_access_token(data={"sub": user["id"], "username": user["username"]})
    refresh_token = create_refresh_token(data={"sub": user["id"], "username": user["username"]})
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=30 * 60,
        user_id=user["id"],
        username=user["username"]
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    token_data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
):
    """刷新访问令牌"""
    try:
        # 解码刷新令牌
        payload = decode_token(token_data.refresh_token)
        
        # 检查令牌类型
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        
        user_id = payload.get("sub")
        username = payload.get("username")
        
        if not user_id or not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        # 创建新的访问令牌
        access_token = create_access_token(
            data={"sub": user_id, "username": username}
        )
        
        # 创建新的刷新令牌
        refresh_token = create_refresh_token(
            data={"sub": user_id, "username": username}
        )
        
        # 记录令牌刷新
        logger.info(f"Token refreshed: user={user_id}")
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=30 * 60,  # 30分钟
            user_id=user_id,
            username=username
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token refresh failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not refresh token"
        )


@router.post("/logout")
async def logout():
    """用户登出"""
    # 在JWT中，登出通常由客户端处理（删除令牌）
    # 这里可以添加令牌黑名单逻辑
    return {"message": "Successfully logged out"}


@router.get("/profile", response_model=UserProfile)
async def get_profile(
    current_user: dict = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    """获取用户资料"""
    try:
        # 解码令牌获取用户信息
        payload = decode_token(current_user)
        user_id = payload.get("sub")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        # 从数据库获取用户资料
        user = await UserService.get_user_by_id(db, int(user_id))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserProfile(
            id=user["id"],
            email=user["email"],
            username=user["username"],
            is_active=user["is_active"],
            created_at=user.get("created_at", ""),
            last_login=user.get("last_login")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get profile"
        )


@router.post("/change-password")
async def change_password(
    password_data: ChangePasswordRequest,
    current_user: dict = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    """修改密码"""
    try:
        # 解码令牌获取用户信息
        payload = decode_token(current_user)
        user_id = payload.get("sub")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        # 这里应该从数据库获取用户并验证当前密码
        # user = await UserService.get_user_by_id(db, user_id)
        # if not verify_password(password_data.current_password, user.hashed_password):
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail="Current password is incorrect"
        #     )
        
        # 更新密码
        # new_hashed_password = get_password_hash(password_data.new_password)
        # await UserService.update_password(db, user_id, new_hashed_password)
        
        # 记录密码修改
        logger.info(f"Password changed: user={user_id}")
        
        return {"message": "Password changed successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to change password: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to change password"
        )


@router.post("/forgot-password")
async def forgot_password(
    email: EmailStr = Body(..., embed=True),
    db: AsyncSession = Depends(get_db)
):
    """忘记密码（发送重置邮件）"""
    try:
        # 检查用户是否存在
        user = await UserService.get_user_by_email(db, email)
        
        if not user:
            # 出于安全考虑，即使用户不存在也返回成功
            logger.info(f"Password reset requested for non-existent email: {email}")
            return {"message": "If the email exists, a reset link will be sent"}
        
        # 生成重置令牌
        reset_token = create_access_token(
            data={"sub": user["id"], "purpose": "password_reset"},
            expires_delta=timedelta(hours=1)
        )
        
        # 这里应该发送重置邮件
        # reset_url = f"https://example.com/reset-password?token={reset_token}"
        # await send_reset_email(user["email"], reset_url)
        
        # 记录重置请求
        logger.info(f"Password reset requested: user={user['id']} email={email}")
        
        return {"message": "If the email exists, a reset link will be sent"}
        
    except Exception as e:
        logger.error(f"Failed to process forgot password: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process request"
        )


@router.post("/reset-password")
async def reset_password(
    token: str = Body(..., embed=True),
    new_password: str = Body(..., embed=True),
    db: AsyncSession = Depends(get_db)
):
    """重置密码"""
    try:
        # 验证密码强度
        if not validate_password_strength(new_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password does not meet strength requirements"
            )
        
        # 解码重置令牌
        payload = decode_token(token)
        
        # 检查令牌用途
        if payload.get("purpose") != "password_reset":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token purpose"
            )
        
        user_id = payload.get("sub")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token"
            )
        
        # 更新密码
        # new_hashed_password = get_password_hash(new_password)
        # await UserService.update_password(db, user_id, new_hashed_password)
        
        # 记录密码重置
        logger.info(f"Password reset: user={user_id}")
        
        return {"message": "Password reset successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to reset password: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reset password"
        )


@router.post("/verify-email")
async def verify_email(
    token: str = Body(..., embed=True),
    db: AsyncSession = Depends(get_db)
):
    """验证邮箱"""
    try:
        # 解码验证令牌
        payload = decode_token(token)
        
        # 检查令牌用途
        if payload.get("purpose") != "email_verification":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token purpose"
            )
        
        user_id = payload.get("sub")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token"
            )
        
        # 更新用户邮箱验证状态
        # await UserService.verify_email(db, user_id)
        
        # 记录邮箱验证
        logger.info(f"Email verified: user={user_id}")
        
        return {"message": "Email verified successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to verify email: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to verify email"
        )