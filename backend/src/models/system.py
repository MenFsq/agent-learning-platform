"""
系统数据模型
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class SystemLog(Base):
    """系统日志模型"""
    __tablename__ = "system_logs"

    id = Column(Integer, primary_key=True, index=True)
    
    # 日志信息
    level = Column(String(20), nullable=False)  # debug, info, warning, error, critical
    module = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)
    details = Column(JSON, default=dict)  # 详细数据
    
    # 用户和请求信息
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    request_path = Column(String(500))
    request_method = Column(String(10))
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<SystemLog(id={self.id}, level='{self.level}', module='{self.module}')>"


class SystemSetting(Base):
    """系统设置模型"""
    __tablename__ = "system_settings"

    id = Column(Integer, primary_key=True, index=True)
    
    # 设置信息
    key = Column(String(100), unique=True, index=True, nullable=False)
    value = Column(JSON, nullable=False)
    data_type = Column(String(50), nullable=False)  # string, number, boolean, array, object
    category = Column(String(100), default="general")
    description = Column(Text)
    
    # 可见性和权限
    is_public = Column(Boolean, default=False, nullable=False)
    is_editable = Column(Boolean, default=True, nullable=False)
    requires_admin = Column(Boolean, default=False, nullable=False)
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    def __repr__(self):
        return f"<SystemSetting(id={self.id}, key='{self.key}', category='{self.category}')>"


class Notification(Base):
    """通知模型"""
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    
    # 接收者信息
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # 通知内容
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String(50), nullable=False)  # info, success, warning, error, system
    category = Column(String(100), default="general")
    
    # 相关实体
    related_type = Column(String(100))  # project, task, user, etc.
    related_id = Column(Integer)
    
    # 动作和链接
    action_url = Column(String(500))
    action_label = Column(String(100))
    
    # 状态
    is_read = Column(Boolean, default=False, nullable=False)
    is_archived = Column(Boolean, default=False, nullable=False)
    priority = Column(String(20), default="normal")  # low, normal, high, urgent
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    read_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<Notification(id={self.id}, user_id={self.user_id}, title='{self.title}')>"


class AuditLog(Base):
    """审计日志模型"""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    
    # 操作信息
    action = Column(String(100), nullable=False)  # create, update, delete, login, logout, etc.
    resource_type = Column(String(100), nullable=False)  # user, project, task, etc.
    resource_id = Column(Integer, nullable=False)
    
    # 变更详情
    old_values = Column(JSON, default=dict)
    new_values = Column(JSON, default=dict)
    changes = Column(JSON, default=dict)  # 具体变更字段
    
    # 执行者信息
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    
    # 请求信息
    request_path = Column(String(500))
    request_method = Column(String(10))
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<AuditLog(id={self.id}, action='{self.action}', resource_type='{self.resource_type}')>"


class FileStorage(Base):
    """文件存储模型"""
    __tablename__ = "file_storage"

    id = Column(Integer, primary_key=True, index=True)
    
    # 文件信息
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)  # 字节
    mime_type = Column(String(100), nullable=False)
    extension = Column(String(50), nullable=False)
    
    # 元数据
    title = Column(String(200))
    description = Column(Text)
    tags = Column(JSON, default=list)
    
    # 所有者和权限
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_public = Column(Boolean, default=False, nullable=False)
    access_token = Column(String(100), unique=True, nullable=True)
    
    # 相关实体
    related_type = Column(String(100))
    related_id = Column(Integer)
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<FileStorage(id={self.id}, filename='{self.filename}', owner_id={self.owner_id})>"