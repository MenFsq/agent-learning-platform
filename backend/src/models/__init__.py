"""
数据库模型包
"""
from .user import User, UserSession, UserRole
from .project import Project, ProjectMember, ProjectTask, ProjectStatus, ProjectType
from .learning import (
    LearningResource, 
    UserLearningProgress, 
    LearningPath, 
    UserLearningPath,
    LearningResourceType
)
from .system import (
    SystemLog, 
    SystemSetting, 
    Notification, 
    AuditLog, 
    FileStorage
)

# 导出所有模型
__all__ = [
    # 用户模型
    "User",
    "UserSession",
    "UserRole",
    
    # 项目模型
    "Project",
    "ProjectMember",
    "ProjectTask",
    "ProjectStatus",
    "ProjectType",
    
    # 学习模型
    "LearningResource",
    "UserLearningProgress",
    "LearningPath",
    "UserLearningPath",
    "LearningResourceType",
    
    # 系统模型
    "SystemLog",
    "SystemSetting",
    "Notification",
    "AuditLog",
    "FileStorage",
]