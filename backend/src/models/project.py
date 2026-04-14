"""
项目数据模型
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship, declarative_base
import enum

Base = declarative_base()


class ProjectStatus(str, enum.Enum):
    """项目状态枚举"""
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class ProjectType(str, enum.Enum):
    """项目类型枚举"""
    LEARNING = "learning"
    DEVELOPMENT = "development"
    RESEARCH = "research"
    PRODUCTION = "production"


class Project(Base):
    """项目模型"""
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, index=True, nullable=False)
    description = Column(Text)
    short_description = Column(String(500))
    
    # 项目元数据
    status = Column(Enum(ProjectStatus), default=ProjectStatus.DRAFT, nullable=False)
    type = Column(Enum(ProjectType), default=ProjectType.LEARNING, nullable=False)
    tags = Column(JSON, default=list)  # 标签列表
    technologies = Column(JSON, default=list)  # 技术栈列表
    
    # 配置和设置
    config = Column(JSON, default=dict)  # 项目配置
    settings = Column(JSON, default=dict)  # 用户设置
    
    # 所有者信息
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", backref="projects")
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # 统计信息
    total_tasks = Column(Integer, default=0)
    completed_tasks = Column(Integer, default=0)
    total_members = Column(Integer, default=1)
    total_contributions = Column(Integer, default=0)
    
    # 可见性
    is_public = Column(Boolean, default=False, nullable=False)
    is_featured = Column(Boolean, default=False, nullable=False)
    
    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}', status='{self.status}')>"


class ProjectMember(Base):
    """项目成员模型"""
    __tablename__ = "project_members"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 成员角色和权限
    role = Column(String(50), default="member", nullable=False)  # owner, admin, member, viewer
    permissions = Column(JSON, default=list)
    
    # 加入信息
    joined_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    invited_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    invitation_token = Column(String(100), nullable=True)
    
    # 状态
    is_active = Column(Boolean, default=True, nullable=False)
    is_accepted = Column(Boolean, default=True, nullable=False)
    
    # 关系
    project = relationship("Project", backref="members")
    user = relationship("User", backref="project_memberships")
    
    def __repr__(self):
        return f"<ProjectMember(id={self.id}, project_id={self.project_id}, user_id={self.user_id})>"


class ProjectTask(Base):
    """项目任务模型"""
    __tablename__ = "project_tasks"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    
    # 任务状态
    status = Column(String(50), default="todo", nullable=False)  # todo, in_progress, review, done
    priority = Column(String(20), default="medium", nullable=False)  # low, medium, high, critical
    
    # 分配和执行
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 时间信息
    due_date = Column(DateTime, nullable=True)
    estimated_hours = Column(Integer, nullable=True)
    actual_hours = Column(Integer, default=0)
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # 标签和分类
    tags = Column(JSON, default=list)
    category = Column(String(100))
    
    # 关系
    project = relationship("Project", backref="tasks")
    
    def __repr__(self):
        return f"<ProjectTask(id={self.id}, title='{self.title}', status='{self.status}')>"