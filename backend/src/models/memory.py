"""
记忆系统数据模型
"""

from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MemoryItem(Base):
    """记忆项模型"""
    __tablename__ = "memory_items"
    
    id = Column(String(64), primary_key=True, comment="记忆项ID")
    content = Column(Text, nullable=False, comment="记忆内容")
    category = Column(String(50), nullable=False, default="general", comment="记忆分类")
    tags = Column(Text, comment="标签列表(JSON格式)")
    importance = Column(Integer, nullable=False, default=1, comment="重要性等级(1-10)")
    relevance_score = Column(Float, default=0.0, comment="相关性分数")
    metadata = Column(Text, comment="元数据(JSON格式)")
    created_at = Column(DateTime, nullable=False, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    def __repr__(self):
        return f"<MemoryItem(id='{self.id}', category='{self.category}', importance={self.importance})>"


class MemorySession(Base):
    """记忆会话模型"""
    __tablename__ = "memory_sessions"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    session_id = Column(String(64), nullable=False, unique=True, comment="会话ID")
    agent_id = Column(String(64), comment="关联的Agent ID")
    context = Column(Text, comment="会话上下文(JSON格式)")
    created_at = Column(DateTime, nullable=False, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    def __repr__(self):
        return f"<MemorySession(session_id='{self.session_id}', agent_id='{self.agent_id}')>"