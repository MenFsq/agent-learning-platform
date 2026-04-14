"""
用户服务层
"""
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_, or_
from sqlalchemy.orm import selectinload
from loguru import logger

from ..models.user import User, UserSession, UserRole
from ..core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
    validate_password_strength
)
from ..schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserLogin,
    UserProfileUpdate
)


class UserService:
    """用户服务类"""
    
    @staticmethod
    async def create_user(
        db: AsyncSession,
        user_data: UserCreate
    ) -> User:
        """
        创建新用户
        """
        try:
            # 检查用户名是否已存在
            existing_user = await db.execute(
                select(User).where(
                    or_(
                        User.username == user_data.username,
                        User.email == user_data.email
                    )
                )
            )
            if existing_user.scalar_one_or_none():
                raise ValueError("Username or email already exists")
            
            # 验证密码强度
            if not validate_password_strength(user_data.password):
                raise ValueError("Password does not meet security requirements")
            
            # 创建用户对象
            user = User(
                email=user_data.email,
                username=user_data.username,
                hashed_password=get_password_hash(user_data.password),
                full_name=user_data.full_name,
                role=UserRole.USER,
                is_active=True,
                is_verified=False,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            db.add(user)
            await db.commit()
            await db.refresh(user)
            
            logger.info(f"User created: {user.username} ({user.email})")
            return user
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Failed to create user: {e}")
            raise
    
    @staticmethod
    async def authenticate_user(
        db: AsyncSession,
        login_data: UserLogin
    ) -> Optional[User]:
        """
        用户认证
        """
        try:
            # 通过用户名或邮箱查找用户
            user = await db.execute(
                select(User).where(
                    or_(
                        User.username == login_data.username,
                        User.email == login_data.username
                    )
                )
            )
            user = user.scalar_one_or_none()
            
            if not user:
                return None
            
            if not verify_password(login_data.password, user.hashed_password):
                return None
            
            if not user.is_active:
                raise ValueError("User account is disabled")
            
            # 更新最后登录时间
            user.last_login = datetime.utcnow()
            await db.commit()
            
            logger.info(f"User authenticated: {user.username}")
            return user
            
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            raise
    
    @staticmethod
    async def get_user_by_id(
        db: AsyncSession,
        user_id: int
    ) -> Optional[User]:
        """
        通过ID获取用户
        """
        try:
            result = await db.execute(
                select(User).where(User.id == user_id)
            )
            return result.scalar_one_or_none()
            
        except Exception as e:
            logger.error(f"Failed to get user by ID: {e}")
            raise
    
    @staticmethod
    async def get_user_by_username(
        db: AsyncSession,
        username: str
    ) -> Optional[User]:
        """
        通过用户名获取用户
        """
        try:
            result = await db.execute(
                select(User).where(User.username == username)
            )
            return result.scalar_one_or_none()
            
        except Exception as e:
            logger.error(f"Failed to get user by username: {e}")
            raise
    
    @staticmethod
    async def get_user_by_email(
        db: AsyncSession,
        email: str
    ) -> Optional[User]:
        """
        通过邮箱获取用户
        """
        try:
            result = await db.execute(
                select(User).where(User.email == email)
            )
            return result.scalar_one_or_none()
            
        except Exception as e:
            logger.error(f"Failed to get user by email: {e}")
            raise
    
    @staticmethod
    async def update_user(
        db: AsyncSession,
        user_id: int,
        update_data: UserUpdate
    ) -> Optional[User]:
        """
        更新用户信息
        """
        try:
            # 获取用户
            user = await UserService.get_user_by_id(db, user_id)
            if not user:
                return None
            
            # 更新字段
            update_dict = update_data.dict(exclude_unset=True)
            
            # 如果更新密码，需要哈希处理
            if "password" in update_dict:
                if not validate_password_strength(update_dict["password"]):
                    raise ValueError("Password does not meet security requirements")
                update_dict["hashed_password"] = get_password_hash(update_dict.pop("password"))
            
            # 移除不允许直接更新的字段
            for field in ["id", "created_at", "last_login"]:
                update_dict.pop(field, None)
            
            # 更新用户
            await db.execute(
                update(User)
                .where(User.id == user_id)
                .values(**update_dict, updated_at=datetime.utcnow())
            )
            await db.commit()
            
            # 重新获取用户
            user = await UserService.get_user_by_id(db, user_id)
            logger.info(f"User updated: {user.username}")
            
            return user
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Failed to update user: {e}")
            raise
    
    @staticmethod
    async def update_user_profile(
        db: AsyncSession,
        user_id: int,
        profile_data: UserProfileUpdate
    ) -> Optional[User]:
        """
        更新用户个人资料
        """
        try:
            # 获取用户
            user = await UserService.get_user_by_id(db, user_id)
            if not user:
                return None
            
            # 更新个人资料字段
            update_dict = profile_data.dict(exclude_unset=True)
            
            await db.execute(
                update(User)
                .where(User.id == user_id)
                .values(**update_dict, updated_at=datetime.utcnow())
            )
            await db.commit()
            
            # 重新获取用户
            user = await UserService.get_user_by_id(db, user_id)
            logger.info(f"User profile updated: {user.username}")
            
            return user
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Failed to update user profile: {e}")
            raise
    
    @staticmethod
    async def delete_user(
        db: AsyncSession,
        user_id: int
    ) -> bool:
        """
        删除用户（软删除）
        """
        try:
            # 获取用户
            user = await UserService.get_user_by_id(db, user_id)
            if not user:
                return False
            
            # 软删除：禁用用户
            await db.execute(
                update(User)
                .where(User.id == user_id)
                .values(is_active=False, updated_at=datetime.utcnow())
            )
            await db.commit()
            
            logger.info(f"User disabled: {user.username}")
            return True
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Failed to delete user: {e}")
            raise
    
    @staticmethod
    async def list_users(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None,
        role: Optional[UserRole] = None
    ) -> List[User]:
        """
        列出用户
        """
        try:
            query = select(User)
            
            # 添加过滤条件
            if is_active is not None:
                query = query.where(User.is_active == is_active)
            
            if role is not None:
                query = query.where(User.role == role)
            
            # 添加分页
            query = query.offset(skip).limit(limit).order_by(User.created_at.desc())
            
            result = await db.execute(query)
            users = result.scalars().all()
            
            return users
            
        except Exception as e:
            logger.error(f"Failed to list users: {e}")
            raise
    
    @staticmethod
    async def search_users(
        db: AsyncSession,
        query: str,
        skip: int = 0,
        limit: int = 50
    ) -> List[User]:
        """
        搜索用户
        """
        try:
            search_query = select(User).where(
                or_(
                    User.username.ilike(f"%{query}%"),
                    User.email.ilike(f"%{query}%"),
                    User.full_name.ilike(f"%{query}%")
                )
            )
            
            search_query = search_query.offset(skip).limit(limit).order_by(User.created_at.desc())
            
            result = await db.execute(search_query)
            users = result.scalars().all()
            
            return users
            
        except Exception as e:
            logger.error(f"Failed to search users: {e}")
            raise
    
    @staticmethod
    async def create_user_session(
        db: AsyncSession,
        user_id: int,
        user_agent: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> Dict[str, str]:
        """
        创建用户会话
        """
        try:
            # 创建访问令牌和刷新令牌
            access_token = create_access_token(data={"sub": str(user_id)})
            refresh_token = create_refresh_token(data={"sub": str(user_id)})
            
            # 创建会话记录
            session = UserSession(
                user_id=user_id,
                session_token=access_token,
                refresh_token=refresh_token,
                user_agent=user_agent,
                ip_address=ip_address,
                expires_at=datetime.utcnow() + timedelta(days=7),
                created_at=datetime.utcnow(),
                last_used_at=datetime.utcnow(),
                is_active=True
            )
            
            db.add(session)
            await db.commit()
            
            logger.info(f"User session created for user_id: {user_id}")
            
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer"
            }
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Failed to create user session: {e}")
            raise
    
    @staticmethod
    async def validate_user_session(
        db: AsyncSession,
        token: str
    ) -> Optional[User]:
        """
        验证用户会话
        """
        try:
            # 解码令牌
            payload = decode_token(token)
            if not payload:
                return None
            
            user_id = int(payload.get("sub"))
            if not user_id:
                return None
            
            # 检查会话是否存在且有效
            session = await db.execute(
                select(UserSession).where(
                    and_(
                        UserSession.session_token == token,
                        UserSession.is_active == True,
                        UserSession.expires_at > datetime.utcnow()
                    )
                )
            )
            session = session.scalar_one_or_none()
            
            if not session:
                return None
            
            # 更新最后使用时间
            session.last_used_at = datetime.utcnow()
            await db.commit()
            
            # 获取用户
            user = await UserService.get_user_by_id(db, user_id)
            if not user or not user.is_active:
                return None
            
            return user
            
        except Exception as e:
            logger.error(f"Failed to validate user session: {e}")
            return None
    
    @staticmethod
    async def revoke_user_session(
        db: AsyncSession,
        token: str
    ) -> bool:
        """
        撤销用户会话
        """
        try:
            # 查找并禁用会话
            result = await db.execute(
                update(UserSession)
                .where(UserSession.session_token == token)
                .values(is_active=False)
            )
            
            await db.commit()
            
            if result.rowcount > 0:
                logger.info(f"User session revoked: {token}")
                return True
            
            return False
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Failed to revoke user session: {e}")
            raise
    
    @staticmethod
    async def refresh_access_token(
        db: AsyncSession,
        refresh_token: str
    ) -> Optional[Dict[str, str]]:
        """
        刷新访问令牌
        """
        try:
            # 验证刷新令牌
            payload = decode_token(refresh_token)
            if not payload:
                return None
            
            user_id = int(payload.get("sub"))
            if not user_id:
                return None
            
            # 检查刷新令牌是否存在且有效
            session = await db.execute(
                select(UserSession).where(
                    and_(
                        UserSession.refresh_token == refresh_token,
                        UserSession.is_active == True,
                        UserSession.expires_at > datetime.utcnow()
                    )
                )
            )
            session = session.scalar_one_or_none()
            
            if not session:
                return None
            
            # 创建新的访问令牌
            new_access_token = create_access_token(data={"sub": str(user_id)})
            
            # 更新会话
            session.session_token = new_access_token
            session.last_used_at = datetime.utcnow()
            await db.commit()
            
            logger.info(f"Access token refreshed for user_id: {user_id}")
            
            return {
                "access_token": new_access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer"
            }
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Failed to refresh access token: {e}")
            raise