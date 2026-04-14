"""
学习资源数据模型
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum, JSON, Float
from sqlalchemy.orm import relationship, declarative_base
import enum

Base = declarative_base()


class LearningResourceType(str, enum.Enum):
    """学习资源类型枚举"""
    ARTICLE = "article"
    VIDEO = "video"
    COURSE = "course"
    TUTORIAL = "tutorial"
    DOCUMENTATION = "documentation"
    EXAMPLE = "example"
    PROJECT = "project"
    CHEATSHEET = "cheatsheet"


class LearningResource(Base):
    """学习资源模型"""
    __tablename__ = "learning_resources"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, index=True, nullable=False)
    description = Column(Text)
    content = Column(Text)  # Markdown内容
    
    # 资源类型和分类
    type = Column(Enum(LearningResourceType), nullable=False)
    category = Column(String(100))
    tags = Column(JSON, default=list)
    difficulty = Column(String(50), default="beginner")  # beginner, intermediate, advanced
    
    # 元数据
    author_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    source_url = Column(String(500))
    estimated_time = Column(Integer)  # 估计学习时间（分钟）
    
    # 统计信息
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    bookmark_count = Column(Integer, default=0)
    average_rating = Column(Float, default=0.0)
    rating_count = Column(Integer, default=0)
    
    # 可见性和状态
    is_published = Column(Boolean, default=False, nullable=False)
    is_featured = Column(Boolean, default=False, nullable=False)
    requires_login = Column(Boolean, default=False, nullable=False)
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    published_at = Column(DateTime, nullable=True)
    
    # 关系
    author = relationship("User", backref="learning_resources")
    
    def __repr__(self):
        return f"<LearningResource(id={self.id}, title='{self.title}', type='{self.type}')>"


class UserLearningProgress(Base):
    """用户学习进度模型"""
    __tablename__ = "user_learning_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resource_id = Column(Integer, ForeignKey("learning_resources.id"), nullable=False)
    
    # 进度信息
    status = Column(String(50), default="not_started")  # not_started, in_progress, completed, abandoned
    progress_percentage = Column(Float, default=0.0)  # 0-100
    current_section = Column(String(200))
    last_position = Column(Integer, default=0)  # 视频位置或文章滚动位置
    
    # 评分和反馈
    user_rating = Column(Integer, nullable=True)  # 1-5
    user_review = Column(Text)
    is_bookmarked = Column(Boolean, default=False)
    
    # 时间信息
    started_at = Column(DateTime, nullable=True)
    last_accessed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    total_time_spent = Column(Integer, default=0)  # 总学习时间（秒）
    
    # 关系
    user = relationship("User", backref="learning_progress")
    resource = relationship("LearningResource", backref="user_progress")
    
    def __repr__(self):
        return f"<UserLearningProgress(id={self.id}, user_id={self.user_id}, resource_id={self.resource_id})>"


class LearningPath(Base):
    """学习路径模型"""
    __tablename__ = "learning_paths"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, index=True, nullable=False)
    description = Column(Text)
    
    # 路径信息
    target_skill = Column(String(200))
    estimated_duration = Column(Integer)  # 估计总时长（小时）
    difficulty_level = Column(String(50), default="beginner")
    prerequisites = Column(JSON, default=list)  # 先决条件列表
    
    # 资源顺序
    resource_order = Column(JSON, default=list)  # 资源ID顺序列表
    
    # 统计信息
    enrolled_count = Column(Integer, default=0)
    completed_count = Column(Integer, default=0)
    average_completion_time = Column(Integer, default=0)
    
    # 可见性和状态
    is_published = Column(Boolean, default=False, nullable=False)
    is_featured = Column(Boolean, default=False, nullable=False)
    
    # 创建者信息
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关系
    creator = relationship("User", backref="created_learning_paths")
    
    def __repr__(self):
        return f"<LearningPath(id={self.id}, name='{self.name}')>"


class UserLearningPath(Base):
    """用户学习路径进度模型"""
    __tablename__ = "user_learning_paths"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    path_id = Column(Integer, ForeignKey("learning_paths.id"), nullable=False)
    
    # 进度信息
    status = Column(String(50), default="not_started")  # not_started, in_progress, completed, paused
    current_resource_index = Column(Integer, default=0)
    completed_resources = Column(JSON, default=list)  # 已完成的资源ID列表
    
    # 统计信息
    progress_percentage = Column(Float, default=0.0)
    total_time_spent = Column(Integer, default=0)  # 总学习时间（秒）
    
    # 时间信息
    enrolled_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    started_at = Column(DateTime, nullable=True)
    last_accessed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    
    # 关系
    user = relationship("User", backref="learning_path_progress")
    path = relationship("LearningPath", backref="user_progress")
    
    def __repr__(self):
        return f"<UserLearningPath(id={self.id}, user_id={self.user_id}, path_id={self.path_id})>"