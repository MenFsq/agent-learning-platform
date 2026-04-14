"""
项目数据模式
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from enum import Enum


class ProjectStatus(str, Enum):
    """项目状态枚举"""
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class ProjectType(str, Enum):
    """项目类型枚举"""
    LEARNING = "learning"
    DEVELOPMENT = "development"
    RESEARCH = "research"
    PRODUCTION = "production"


# 基础模型
class ProjectBase(BaseModel):
    """项目基础模型"""
    name: str = Field(..., min_length=1, max_length=200)
    slug: str = Field(..., min_length=1, max_length=200, regex=r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
    description: Optional[str] = None
    short_description: Optional[str] = Field(None, max_length=500)
    
    @validator('slug')
    def validate_slug(cls, v):
        # 确保slug是URL友好的
        if not v.replace('-', '').isalnum():
            raise ValueError('Slug can only contain letters, numbers, and hyphens')
        return v.lower()


# 创建模型
class ProjectCreate(ProjectBase):
    """项目创建模型"""
    type: Optional[ProjectType] = ProjectType.LEARNING
    tags: Optional[List[str]] = []
    technologies: Optional[List[str]] = []
    config: Optional[Dict[str, Any]] = {}
    settings: Optional[Dict[str, Any]] = {}
    is_public: Optional[bool] = False


# 更新模型
class ProjectUpdate(BaseModel):
    """项目更新模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    slug: Optional[str] = Field(None, min_length=1, max_length=200, regex=r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
    description: Optional[str] = None
    short_description: Optional[str] = Field(None, max_length=500)
    status: Optional[ProjectStatus] = None
    type: Optional[ProjectType] = None
    tags: Optional[List[str]] = None
    technologies: Optional[List[str]] = None
    config: Optional[Dict[str, Any]] = None
    settings: Optional[Dict[str, Any]] = None
    is_public: Optional[bool] = None
    is_featured: Optional[bool] = None
    
    @validator('slug')
    def validate_slug(cls, v):
        if v is not None:
            if not v.replace('-', '').isalnum():
                raise ValueError('Slug can only contain letters, numbers, and hyphens')
            return v.lower()
        return v


# 响应模型
class ProjectResponse(ProjectBase):
    """项目响应模型"""
    id: int
    status: ProjectStatus
    type: ProjectType
    tags: List[str]
    technologies: List[str]
    config: Dict[str, Any]
    settings: Dict[str, Any]
    owner_id: int
    created_at: datetime
    updated_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    total_tasks: int
    completed_tasks: int
    total_members: int
    total_contributions: int
    is_public: bool
    is_featured: bool
    
    class Config:
        from_attributes = True


# 项目成员模型
class ProjectMemberBase(BaseModel):
    """项目成员基础模型"""
    role: str = Field(default="member", max_length=50)
    permissions: Optional[List[str]] = []


class ProjectMemberCreate(ProjectMemberBase):
    """项目成员创建模型"""
    user_id: int
    invitation_token: Optional[str] = None
    is_accepted: Optional[bool] = False


class ProjectMemberUpdate(BaseModel):
    """项目成员更新模型"""
    role: Optional[str] = Field(None, max_length=50)
    permissions: Optional[List[str]] = None
    is_active: Optional[bool] = None


class ProjectMemberResponse(ProjectMemberBase):
    """项目成员响应模型"""
    id: int
    project_id: int
    user_id: int
    joined_at: datetime
    invited_by: Optional[int]
    is_active: bool
    is_accepted: bool
    
    class Config:
        from_attributes = True


# 项目任务模型
class ProjectTaskBase(BaseModel):
    """项目任务基础模型"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[str] = Field(default="todo", max_length=50)
    priority: Optional[str] = Field(default="medium", max_length=20)
    assigned_to: Optional[int] = None
    due_date: Optional[datetime] = None
    estimated_hours: Optional[int] = Field(None, ge=0)
    tags: Optional[List[str]] = []
    category: Optional[str] = Field(None, max_length=100)


class ProjectTaskCreate(ProjectTaskBase):
    """项目任务创建模型"""
    pass


class ProjectTaskUpdate(BaseModel):
    """项目任务更新模型"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[str] = Field(None, max_length=50)
    priority: Optional[str] = Field(None, max_length=20)
    assigned_to: Optional[int] = None
    due_date: Optional[datetime] = None
    estimated_hours: Optional[int] = Field(None, ge=0)
    actual_hours: Optional[int] = Field(None, ge=0)
    tags: Optional[List[str]] = None
    category: Optional[str] = Field(None, max_length=100)


class ProjectTaskResponse(ProjectTaskBase):
    """项目任务响应模型"""
    id: int
    project_id: int
    created_by: int
    actual_hours: int
    created_at: datetime
    updated_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# 项目统计模型
class ProjectStats(BaseModel):
    """项目统计模型"""
    project: Dict[str, Any]
    tasks: Dict[str, Any]
    members: Dict[str, Any]
    overall: Dict[str, Any]


# 项目列表响应
class ProjectListResponse(BaseModel):
    """项目列表响应模型"""
    total: int
    projects: List[ProjectResponse]
    page: int
    page_size: int
    total_pages: int


# 项目搜索响应
class ProjectSearchResponse(BaseModel):
    """项目搜索响应模型"""
    query: str
    results: List[ProjectResponse]
    total: int
    page: int
    page_size: int


# 项目邀请模型
class ProjectInviteCreate(BaseModel):
    """项目邀请创建模型"""
    email: str
    role: str = Field(default="member", max_length=50)
    permissions: Optional[List[str]] = []
    message: Optional[str] = None


class ProjectInviteResponse(BaseModel):
    """项目邀请响应模型"""
    id: int
    project_id: int
    email: str
    role: str
    permissions: List[str]
    invited_by: int
    invited_at: datetime
    expires_at: datetime
    is_accepted: bool
    token: str
    
    class Config:
        from_attributes = True