"""
技能管理数据模型
"""

from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SkillTrial(Base):
    """技能试用记录模型"""
    __tablename__ = "skill_trials"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    trial_id = Column(String(64), nullable=False, unique=True, comment="试用ID")
    skill_name = Column(String(100), nullable=False, comment="技能名称")
    skill_version = Column(String(50), comment="技能版本")
    parameters = Column(Text, comment="试用参数(JSON格式)")
    status = Column(String(20), nullable=False, default="pending", comment="状态: pending, running, completed, failed")
    timeout_seconds = Column(Integer, default=300, comment="超时时间(秒)")
    started_at = Column(DateTime, nullable=False, default=datetime.now, comment="开始时间")
    completed_at = Column(DateTime, comment="完成时间")
    error_message = Column(Text, comment="错误信息")
    created_at = Column(DateTime, nullable=False, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    def __repr__(self):
        return f"<SkillTrial(trial_id='{self.trial_id}', skill='{self.skill_name}', status='{self.status}')>"


class SkillReport(Base):
    """技能试用报告模型"""
    __tablename__ = "skill_reports"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    report_id = Column(String(64), nullable=False, unique=True, comment="报告ID")
    trial_id = Column(String(64), nullable=False, comment="关联的试用ID")
    skill_name = Column(String(100), nullable=False, comment="技能名称")
    skill_version = Column(String(50), comment="技能版本")
    status = Column(String(20), nullable=False, default="pending", comment="状态: pending, analyzing, completed")
    score = Column(Float, comment="评估分数(0-1)")
    metrics = Column(Text, comment="性能指标(JSON格式)")
    evaluation = Column(Text, comment="评估结果(JSON格式)")
    recommendations = Column(Text, comment="推荐建议(JSON格式)")
    created_at = Column(DateTime, nullable=False, default=datetime.now, comment="创建时间")
    completed_at = Column(DateTime, comment="完成时间")
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    def __repr__(self):
        return f"<SkillReport(report_id='{self.report_id}', skill='{self.skill_name}', score={self.score})>"